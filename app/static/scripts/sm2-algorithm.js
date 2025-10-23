/**
 * Enhanced Spaced Repetition Algorithm (Improved SM2)
 * 
 * This file contains the SM2 spaced repetition algorithm implementation
 * and related helper functions for optimal learning scheduling.
 * 
 * @author Flasheeta Development Team
 * @version 2.0
 */

/**
 * Enhanced SM2 Algorithm Implementation
 * 
 * @param {Object} progress - Current progress object containing review history
 * @param {string} rating - User's difficulty rating ('again', 'hard', 'good', 'easy')
 * @returns {Object} Updated progress object with new scheduling information
 */
function sm2Algorithm(progress, rating) {
    let { review_count, correct_count, ease_factor, interval, last_review_date } = progress;

    // Ensure we have valid defaults
    review_count = review_count || 0;
    correct_count = correct_count || 0;
    ease_factor = ease_factor || 2.5;
    interval = interval || 1;
    last_review_date = new Date(last_review_date || new Date());

    // Enhanced rating system with more precise values
    const ratings = {
        again: 0,    // Complete blackout
        hard: 2,     // Incorrect response, but remembered upon seeing answer
        good: 3,     // Correct response with serious difficulty
        easy: 5      // Perfect response
    };

    const quality = ratings[rating];
    
    // Validate quality rating
    if (quality === undefined) {
        console.error('Invalid rating:', rating);
        return progress; // Return unchanged if invalid rating
    }

    // Update last review date to current time
    const current_time = new Date();
    last_review_date = current_time;

    // Track statistics
    review_count++;
    if (quality >= 3) {
        correct_count++;
    }

    // Standard SM2 Algorithm Implementation
    if (quality < 3) {
        // Failed recall - reset to beginning with 1 day interval
        interval = 1;
        ease_factor = Math.max(1.3, ease_factor - 0.2);
    } else {
        // Successful recall - calculate new interval
        if (review_count === 1) {
            interval = 1;
        } else if (review_count === 2) {
            interval = 6;
        } else {
            // Apply ease factor with quality-based multiplier
            const qualityMultiplier = {
                2: 0.85, // Hard: slower progression
                3: 1.0,  // Good: normal progression
                5: 1.3   // Easy: accelerated progression
            }[quality] || 1.0;
            
            interval = Math.round(interval * ease_factor * qualityMultiplier);
        }

        // Standard SM2 ease factor calculation
        ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
    }

    // Apply bounds to ease factor
    ease_factor = Math.max(1.3, Math.min(ease_factor, 2.5));
    
    // Apply bounds to interval
    interval = Math.max(1, Math.min(interval, 365)); // Max 1 year

    // Calculate next review date using consistent day-based intervals
    let next_review_date = new Date(current_time);
    next_review_date.setDate(next_review_date.getDate() + interval);

    // Log for debugging (can be removed in production)
    console.log(`SM2 Update: Rating=${rating}, Quality=${quality}, Interval=${interval}, EF=${ease_factor.toFixed(2)}, Next=${next_review_date.toISOString()}`);

    return {
        review_count,
        correct_count,
        ease_factor: Math.round(ease_factor * 100) / 100, // Round to 2 decimal places
        interval,
        last_review_date: last_review_date.toISOString(),
        next_review_date: next_review_date.toISOString(),
        difficulty_rating: rating // Store the original rating for reference
    };
}

/**
 * Get human-readable description of when the next review is due
 * 
 * @param {string|Date} next_review_date - The next review date
 * @returns {string} Human-readable description (e.g., "Due in 3 days")
 */
function getNextReviewDescription(next_review_date) {
    const now = new Date();
    const nextReview = new Date(next_review_date);
    const diffMs = nextReview - now;
    
    if (diffMs <= 0) {
        return "Due now";
    }
    
    const diffMinutes = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    
    if (diffDays > 0) {
        return `Due in ${diffDays} day${diffDays > 1 ? 's' : ''}`;
    } else if (diffHours > 0) {
        return `Due in ${diffHours} hour${diffHours > 1 ? 's' : ''}`;
    } else {
        return `Due in ${diffMinutes} minute${diffMinutes > 1 ? 's' : ''}`;
    }
}

/**
 * Validate and ensure progress object has all required fields with defaults
 * 
 * @param {Object} progress - Progress object to validate
 * @returns {Object} Validated progress object with all required fields
 */
function validateProgress(progress) {
    const defaults = {
        review_count: 0,
        correct_count: 0,
        ease_factor: 2.5,
        interval: 1,
        last_review_date: new Date().toISOString(),
        next_review_date: new Date().toISOString(),
        difficulty_rating: 'good'
    };
    
    return { ...defaults, ...progress };
}

/**
 * Calculate learning statistics from progress data
 * 
 * @param {Object} progress - Progress object containing review history
 * @returns {Object} Learning statistics including accuracy, difficulty, and review count
 */
function calculateLearningStats(progress) {
    const { review_count, correct_count, ease_factor } = progress;
    const accuracy = review_count > 0 ? (correct_count / review_count * 100).toFixed(1) : 0;
    const difficulty = ease_factor < 2.0 ? 'Hard' : ease_factor > 2.7 ? 'Easy' : 'Medium';
    
    return {
        accuracy: `${accuracy}%`,
        difficulty,
        reviews: review_count
    };
}

/**
 * Check if a flashcard is due for review
 * 
 * @param {string|Date} next_review_date - The scheduled next review date
 * @returns {boolean} True if the card is due for review
 */
function isCardDueForReview(next_review_date) {
    const now = new Date();
    const nextReview = new Date(next_review_date);
    return now >= nextReview;
}

/**
 * Get recommended study schedule based on current progress
 * 
 * @param {Array} flashcards - Array of flashcard progress objects
 * @returns {Object} Study schedule with due and upcoming cards
 */
function getStudySchedule(flashcards) {
    const now = new Date();
    const dueCards = [];
    const upcomingCards = [];
    
    flashcards.forEach(card => {
        const nextReview = new Date(card.next_review_date);
        if (now >= nextReview) {
            dueCards.push(card);
        } else {
            upcomingCards.push(card);
        }
    });
    
    // Sort due cards by priority (oldest due first)
    dueCards.sort((a, b) => new Date(a.next_review_date) - new Date(b.next_review_date));
    
    // Sort upcoming cards by next review date
    upcomingCards.sort((a, b) => new Date(a.next_review_date) - new Date(b.next_review_date));
    
    return {
        dueCards,
        upcomingCards,
        totalDue: dueCards.length,
        nextReview: upcomingCards.length > 0 ? upcomingCards[0].next_review_date : null
    };
}

// Export functions for use in other files (if using modules)
// Uncomment if using ES6 modules:
// export { sm2Algorithm, getNextReviewDescription, validateProgress, calculateLearningStats, isCardDueForReview, getStudySchedule };