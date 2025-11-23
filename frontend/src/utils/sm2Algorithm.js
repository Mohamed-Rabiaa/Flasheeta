import { RATINGS, CONFIG } from './constants';

/**
 * SM2 Algorithm implementation (Hybrid approach)
 * Uses fixed intervals for failed cards, adaptive SM2 for successful cards
 */
export const sm2Algorithm = (progress, rating) => {
  const quality = RATINGS[rating.toUpperCase()];
  
  // Current values
  const reviewCount = progress.review_count + 1;
  const correctCount = progress.correct_count + (quality >= 3 ? 1 : 0);
  let easeFactor = progress.ease_factor || CONFIG.SM2.INITIAL_EASE_FACTOR;
  let interval = progress.interval || 1;
  
  // Hybrid approach: Fixed intervals for failed, SM2 for successful
  if (quality < 3) {
    // Failed cards - fixed short intervals
    if (quality === 0) {
      interval = CONFIG.INTERVALS.AGAIN / (24 * 60); // Convert minutes to days
    } else {
      interval = CONFIG.INTERVALS.HARD / (24 * 60); // Convert minutes to days
    }
    
    easeFactor = Math.max(CONFIG.SM2.MIN_EASE_FACTOR, easeFactor - 0.2);
  } else {
    // Successful cards - adaptive SM2
    if (reviewCount === 1) {
      interval = 1; // 1 day
    } else if (reviewCount === 2) {
      interval = 6; // 6 days
    } else {
      const multiplier = quality === 5 ? 1.3 : 1.0;
      interval = Math.round(interval * easeFactor * multiplier);
    }
    
    // Update ease factor
    easeFactor = easeFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
  }
  
  // Apply bounds
  easeFactor = Math.max(CONFIG.SM2.MIN_EASE_FACTOR, Math.min(easeFactor, CONFIG.SM2.MAX_EASE_FACTOR));
  interval = Math.max(CONFIG.INTERVALS.AGAIN / (24 * 60), Math.min(interval, 365));
  
  // Calculate next review date
  const intervalMs = interval * 24 * 60 * 60 * 1000;
  const nextReviewDate = new Date(Date.now() + intervalMs);
  
  return {
    review_count: reviewCount,
    correct_count: correctCount,
    ease_factor: parseFloat(easeFactor.toFixed(2)),
    interval: interval,
    last_review_date: new Date().toISOString(),
    next_review_date: nextReviewDate.toISOString(),
    difficulty_rating: rating,
  };
};

/**
 * Calculate learning statistics
 */
export const calculateLearningStats = (progress) => {
  const accuracy = progress.review_count > 0 
    ? (progress.correct_count / progress.review_count * 100).toFixed(1)
    : 0;
    
  return {
    accuracy: `${accuracy}%`,
    reviews: progress.review_count,
    correct: progress.correct_count,
  };
};

/**
 * Get human-readable next review description
 */
export const getNextReviewDescription = (nextReviewDate) => {
  const now = new Date();
  const next = new Date(nextReviewDate);
  const diffMs = next - now;
  const diffMinutes = Math.round(diffMs / (1000 * 60));
  const diffHours = Math.round(diffMs / (1000 * 60 * 60));
  const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));
  
  if (diffMinutes < 60) {
    return `${diffMinutes} minutes`;
  } else if (diffHours < 24) {
    return `${diffHours} hours`;
  } else if (diffDays === 1) {
    return 'tomorrow';
  } else {
    return `${diffDays} days`;
  }
};

/**
 * Validate progress object
 */
export const validateProgress = (progress) => {
  return {
    review_count: progress.review_count || 0,
    correct_count: progress.correct_count || 0,
    ease_factor: progress.ease_factor || CONFIG.SM2.INITIAL_EASE_FACTOR,
    interval: progress.interval || 1,
    last_review_date: progress.last_review_date || new Date().toISOString(),
    next_review_date: progress.next_review_date || new Date().toISOString(),
    difficulty_rating: progress.difficulty_rating || null,
  };
};
