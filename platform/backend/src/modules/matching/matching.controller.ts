import { Body, Controller, Get, Post } from '@nestjs/common';
import { MatchingService } from './matching.service';
import { MatchingRequestDto, MatchingResponseDto } from './dto/matching.dto';

/**
 * U-CS 2 — Intelligent Mentor Matching
 * Built and hosted by: the assigned team
 *
 * This is an ADAPTER. The logic lives in their service; we call it.
 * Their URL is configured as MATCHING_SERVICE_URL.
 */
@Controller('matching')
export class MatchingController {
  constructor(private readonly service: MatchingService) {}

  @Post('match')
  async handle(@Body() body: MatchingRequestDto): Promise<MatchingResponseDto> {
    return this.service.call(body);
  }

  /** Is their service up? Useful before a demo. */
  @Get('status')
  async status() {
    return this.service.status();
  }
}
