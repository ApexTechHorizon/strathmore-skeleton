import { Body, Controller, Get, Post } from '@nestjs/common';
import { CareerPathService } from './career-path.service';
import { CareerPathRequestDto, CareerPathResponseDto } from './dto/career-path.dto';

/**
 * U-CS 1 — AI Career Path Recommendation
 * Built and hosted by: the assigned team
 *
 * This is an ADAPTER. The logic lives in their service; we call it.
 * Their URL is configured as CAREER_PATH_SERVICE_URL.
 */
@Controller('career-path')
export class CareerPathController {
  constructor(private readonly service: CareerPathService) {}

  @Post('paths')
  async handle(@Body() body: CareerPathRequestDto): Promise<CareerPathResponseDto> {
    return this.service.call(body);
  }

  /** Is their service up? Useful before a demo. */
  @Get('status')
  async status() {
    return this.service.status();
  }
}
