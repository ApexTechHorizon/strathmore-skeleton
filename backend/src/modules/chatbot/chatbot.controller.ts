import { Body, Controller, Get, Post } from '@nestjs/common';
import { ChatbotService } from './chatbot.service';
import { ChatbotRequestDto, ChatbotResponseDto } from './dto/chatbot.dto';

/**
 * U-CS 4 — AI Career Coaching Chatbot
 * Built and hosted by: the assigned team
 *
 * This is an ADAPTER. The logic lives in their service; we call it.
 * Their URL is configured as CHATBOT_SERVICE_URL.
 */
@Controller('chatbot')
export class ChatbotController {
  constructor(private readonly service: ChatbotService) {}

  @Post('ask')
  async handle(@Body() body: ChatbotRequestDto): Promise<ChatbotResponseDto> {
    return this.service.call(body);
  }

  /** Is their service up? Useful before a demo. */
  @Get('status')
  async status() {
    return this.service.status();
  }
}
