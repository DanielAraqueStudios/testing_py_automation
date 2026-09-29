import { CanActivateFn } from '@angular/router';

// TODO: verify the Clerk session JWT here (see ARCHITECTURE.md section 6) and
// redirect to the Clerk sign-in flow when the visitor has no valid session.
// No real Clerk SDK integration yet — this is a structural placeholder.
export const authGuard: CanActivateFn = () => {
  return true;
};
