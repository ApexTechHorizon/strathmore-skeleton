/**
 * U-CS 5 — the agreed shapes.
 *
 * Fixed by the Team Integration Map v0.1. Changing them breaks: analytics (U-CS 7)
 */

export class SessionValueRequestDto {
  // in : { menteeId, mentorId, leadTimeHours, hasAgenda, isFirstSession }
}

export class SessionValueResponseDto {
  // out: { probability, factors[], suggestedIntervention }
}
