import { HttpException, Injectable, Logger } from '@nestjs/common';
import { ChatbotRequestDto, ChatbotResponseDto } from './dto/chatbot.dto';

/**
 * U-CS 4 — adapter for the service built by the assigned team.
 *
 * We do not implement the logic. We call their hosted URL and pass the answer on.
 * Free hosting sleeps, so the first call after a quiet period can be slow — hence
 * the generous timeout.
 */
@Injectable()
export class ChatbotService {
  private readonly log = new Logger(ChatbotService.name);
  private readonly baseUrl = process.env.CHATBOT_SERVICE_URL ?? '';
  private readonly timeoutMs = Number(process.env.STUDENT_SERVICE_TIMEOUT_MS ?? 30000);

  async call(body: ChatbotRequestDto): Promise<ChatbotResponseDto> {
    if (!this.baseUrl) {
      throw new HttpException('chatbot: CHATBOT_SERVICE_URL is not set — no service URL yet', 503);
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const res = await fetch(`${this.baseUrl}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      if (!res.ok) {
        throw new HttpException(`chatbot: upstream returned ${res.status}`, 502);
      }
      return (await res.json()) as ChatbotResponseDto;
    } catch (err) {
      this.log.error(`chatbot upstream failed: ${err}`);
      throw new HttpException('chatbot: upstream unavailable', 502);
    } finally {
      clearTimeout(timer);
    }
  }

  async status() {
    if (!this.baseUrl) return { module: 'chatbot', configured: false };
    try {
      const res = await fetch(`${this.baseUrl}/health`);
      return { module: 'chatbot', configured: true, up: res.ok, url: this.baseUrl };
    } catch {
      return { module: 'chatbot', configured: true, up: false, url: this.baseUrl };
    }
  }
}
