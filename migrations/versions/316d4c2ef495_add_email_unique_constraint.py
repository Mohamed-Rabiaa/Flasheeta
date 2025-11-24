"""add email unique constraint

Revision ID: 316d4c2ef495
Revises: 4565b75561a7
Create Date: 2025-11-24 21:26:22.181328

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, select, text


# revision identifiers, used by Alembic.
revision = '316d4c2ef495'
down_revision = '4565b75561a7'
branch_labels = None
depends_on = None


def upgrade():
    # Check if email column exists, if not add it
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    columns = [col['name'] for col in inspector.get_columns('users')]
    
    if 'email' not in columns:
        # Add email column as nullable first
        with op.batch_alter_table('users', schema=None) as batch_op:
            batch_op.add_column(sa.Column('email', sa.String(length=128), nullable=True))
        
        # Update existing users with unique placeholder emails
        users_table = table('users',
            column('id', String),
            column('name', String),
            column('email', String)
        )
        
        users = connection.execute(select(users_table.c.id, users_table.c.name)).fetchall()
        
        for user in users:
            connection.execute(
                users_table.update().where(users_table.c.id == user.id).values(
                    email=f"{user.name}@flasheeta.local"
                )
            )
        
        # Make email NOT NULL
        with op.batch_alter_table('users', schema=None) as batch_op:
            batch_op.alter_column('email', nullable=False)
    else:
        # Email column exists, check if there are empty emails
        result = connection.execute(text("SELECT COUNT(*) FROM users WHERE email IS NULL OR email = ''"))
        count = result.scalar()
        
        if count > 0:
            # Update empty emails
            users_table = table('users',
                column('id', String),
                column('name', String),
                column('email', String)
            )
            
            users = connection.execute(
                text("SELECT id, name FROM users WHERE email IS NULL OR email = ''")
            ).fetchall()
            
            for user in users:
                connection.execute(
                    text("UPDATE users SET email = :email WHERE id = :id"),
                    {"email": f"{user.name}@flasheeta.local", "id": user.id}
                )
    
    # Add unique constraint
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_users_email', ['email'])


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('uq_users_email', type_='unique')
