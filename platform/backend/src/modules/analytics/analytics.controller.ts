import { Body, Controller, Get, Post } from '@nestjs/common';
import { AnalyticsService } from './analytics.service';
import { AnalyticsRequestDto, AnalyticsResponseDto } from './dto/analytics.dto';

/**
 * U-CS 7 — Institution Impact Analytics
 * Built and hosted by: the assigned team
 *
 * This is an ADAPTER. The logic lives in their service; we call it.
 * Their URL is configured as ANALYTICS_SERVICE_URL.
 */
@Controller('analytics')
export class AnalyticsController {
  constructor(private readonly service: AnalyticsService) {}

  @Post('cohort')
  async handle(@Body() body: AnalyticsRequestDto): Promise<AnalyticsResponseDto> {
    return this.service.call(body);
  }

  /** Is their service up? Useful before a demo. */
  @Get('status')
  async status() {
    return this.service.status();
  }
}
