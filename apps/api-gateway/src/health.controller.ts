import { Controller, Get } from '@nestjs/common';

// TODO(auth): once Clerk JWT verification is added, this controller stays
// public while every other route gets a service-to-service/user JWT guard.
@Controller('health')
export class HealthController {
  @Get()
  check() {
    return { status: 'ok', service: 'api-gateway' };
  }
}
