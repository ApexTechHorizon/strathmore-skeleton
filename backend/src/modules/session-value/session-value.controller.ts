import { Body, Controller, Get, Post } from '@nestjs/common';
import { SessionValueService } from './session-value.service';
import { SessionValueRequestDto, SessionValueResponseDto } from './dto/session-value.dto';

/**
 * U-CS 5 — Session Effectiveness Predictor
 * Built and hosted by: the assigned team
 *
 * This is an ADAPTER. The logic lives in their service; we call it.
 * Their URL is configured as SESSION_VALUE_SERVICE_URL.
 */
@Controller('session-value')
export class SessionValueController {
  constructor(private readonly service: SessionValueService) {}

  @Post('predict')
  async handle(@Body() body: SessionValueRequestDto): Promise<SessionValueResponseDto> {
    return this.service.call(body);
  }

  /** Is their service up? Useful before a demo. */
  @Get('status')
  async status() {
    return this.service.status();
  }
}
