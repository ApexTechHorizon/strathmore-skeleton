import { Body, Controller, Get, Post } from '@nestjs/common';
import { MicroLearningService } from './micro-learning.service';
import { MicroLearningRequestDto, MicroLearningResponseDto } from './dto/micro-learning.dto';

/**
 * U-CS 8 — Micro-Learning Recommendation
 * Built and hosted by: the assigned team
 *
 * This is an ADAPTER. The logic lives in their service; we call it.
 * Their URL is configured as MICRO_LEARNING_SERVICE_URL.
 */
@Controller('micro-learning')
export class MicroLearningController {
  constructor(private readonly service: MicroLearningService) {}

  @Post('next')
  async handle(@Body() body: MicroLearningRequestDto): Promise<MicroLearningResponseDto> {
    return this.service.call(body);
  }

  /** Is their service up? Useful before a demo. */
  @Get('status')
  async status() {
    return this.service.status();
  }
}
