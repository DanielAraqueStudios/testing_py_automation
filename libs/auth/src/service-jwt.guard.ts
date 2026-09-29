import { CanActivate, ExecutionContext, Injectable } from '@nestjs/common';

/**
 * STUB — placeholder for the guard that verifies short-lived internal
 * service-to-service JWTs (e.g. api-gateway -> crm-service).
 *
 * TODO: verify the internal signing secret/JWKS and confirm the issuing
 * service identity against an allowlist.
 */
@Injectable()
export class ServiceJwtGuard implements CanActivate {
  canActivate(_context: ExecutionContext): boolean {
    throw new Error('ServiceJwtGuard is a stub and is not implemented yet');
  }
}
