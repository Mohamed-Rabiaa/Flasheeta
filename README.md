# Flasheeta

A flashcard web application.

## Introduction

Flasheeta is a flashcard website where users can create flashcards and review them. You can visit the live website [here](https://flasheeta.pythonanywhere.com).

Read the final [project blog article](https://www.linkedin.com/posts/mohamed-rabiaa_the-story-behind-flasheeta-i-am-thrilled-activity-7216388400952578048-Z8uG?utm_source=share&utm_medium=member_desktop).

Connect with me on [LinkedIn](https://www.linkedin.com/in/mohamed-rabiaa/).

## Installation

1. Clone the project repository:
   ```bash
   git clone https://github.com/Mohamed-Rabiaa/Flasheeta.git
   cd Flasheeta

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt

3. Set the environment variables:
   * `SECRET_KEY`: You can generate one using `os.urandom(24).hex()`.  
   * `DATABASE_URL`: Your database URL, e.g., `mysql://username:password@localhost/dbname`.

4. Run database migrations:
   ```bash
   flask db upgrade

## Usage
1. Register:
   
   * New users need to register by clicking the "Register Now" link on the login page.

  ![Register Page](https://github.com/Mohamed-Rabiaa/Flasheeta/assets/79233929/b05bbfcd-5dae-4d96-9562-878155ad6929)

2. Create Flashcards:

    * Go to the "New Flashcard" page to add a new deck and new flashcards.
      
![New flashcard page](https://github.com/Mohamed-Rabiaa/Flasheeta/assets/79233929/f9b14193-b81f-423b-92d3-988dee52ef8d)

3. Review Flashcards:

   * Go to the "Decks" page, click on a deck’s name, and review the flashcards one by one.
     
![show flashcard page](https://github.com/Mohamed-Rabiaa/Flasheeta/assets/79233929/fd149a2b-5ba0-4580-b760-0e130c4bfb21)



  * Rate each flashcard based on how well you recalled the answer. The rating determines when the card will be shown again.

## Contributing
Contributions are welcome! To contribute:

1. Find a bug or suggest a new feature.
2. Clone the project, make your changes, and commit them.
3. Create a pull request.

## Related Projects
[Anki](https://github.com/ankitects/anki):  A powerful, cross-platform flashcard application.

## Licensing
Flasheeta © 2024 by Mohamed Rabiaa is licensed under CC BY-NC 4.0. For more details, visit the [license page](https://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1).





