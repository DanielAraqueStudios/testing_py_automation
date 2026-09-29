import { CanActivate, ExecutionContext, Injectable } from '@nestjs/common';

/**
 * STUB — placeholder for the guard that verifies inbound Clerk JWTs
 * (client-portal / marketing-site -> api-gateway) via Clerk's JWKS endpoint.
 *
 * TODO: fetch and cache Clerk's JWKS, verify the Bearer token signature/claims,
 * and attach the resolved user/org to the request.
 */
@Injectable()
export class ClerkJwtGuard implements CanActivate {
  canActivate(_context: ExecutionContext): boolean {
    throw new Error('ClerkJwtGuard is a stub and is not implemented yet');
  }
}
