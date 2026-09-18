/**
 * U-CS 2 — the agreed shapes.
 *
 * Fixed by the Team Integration Map v0.1. Changing them breaks: session-value (U-CS 5), pricing (U-CS 6), analytics (U-CS 7)
 */

export class MatchingRequestDto {
  // in : { menteeId, needs: { budgetMax, timeframeWeeks, language } }
}

export class MatchingResponseDto {
  // out: { mentors: [{ mentorId, score, reason }] }
}
