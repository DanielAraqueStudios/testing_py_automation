import {
  SubscribeMessage,
  WebSocketGateway,
  WebSocketServer,
  MessageBody,
} from '@nestjs/websockets';
import { Server } from 'socket.io';

// TODO(auth): verify Clerk/service JWT on connection handshake before
// accepting subscriptions (client-portal connects directly, not via api-gateway).
@WebSocketGateway({ cors: true })
export class ProgressGateway {
  @WebSocketServer()
  server: Server;

  @SubscribeMessage('progress:subscribe')
  handleSubscribe(@MessageBody() payload: { dealId: string }) {
    // Placeholder: future work joins a room per dealId and pushes updates
    // from crm-service via a queue consumer.
    return { subscribed: payload?.dealId ?? null };
  }
}
