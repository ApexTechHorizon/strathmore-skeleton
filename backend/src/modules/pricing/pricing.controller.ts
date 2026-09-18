import { Body, Controller, Get, Post } from '@nestjs/common';
import { PricingService } from './pricing.service';
import { PricingRequestDto, PricingResponseDto } from './dto/pricing.dto';

/**
 * U-CS 6 — AI Pricing Optimization
 * Built and hosted by: the assigned team
 *
 * This is an ADAPTER. The logic lives in their service; we call it.
 * Their URL is configured as PRICING_SERVICE_URL.
 */
@Controller('pricing')
export class PricingController {
  constructor(private readonly service: PricingService) {}

  @Post('price')
  async handle(@Body() body: PricingRequestDto): Promise<PricingResponseDto> {
    return this.service.call(body);
  }

  /** Is their service up? Useful before a demo. */
  @Get('status')
  async status() {
    return this.service.status();
  }
}
