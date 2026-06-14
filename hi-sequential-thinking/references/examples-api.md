# Example: API Design with Sequential Thinking

**Problem**: Design authentication API for multi-tenant SaaS.

```
Thought 1/5: Requirements
Multi-tenant SaaS auth: tenant isolation, scalability, security.
Uncertainty: Session vs token? Next: Evaluate approaches.

Thought 2/6: Approach evaluation (adjusted)
- Session: Server state, easy revocation, harder scaling
- JWT: Stateless, scales well, complex revocation
Multi-tenancy complicates sessions. JWT better for distributed.

Thought 3/6: JWT payload design
JWT includes: User ID, Tenant ID, Permissions, Expiration.
Uncertainty: Where verify tenant? Gateway vs service?

Thought 4/6 [REVISION of Thought 3]: Security fix
- Original: Tenant ID in JWT claims
- Issue: Claims visible (base64), could read tenant IDs
- Corrected: Keep tenant ID, add gateway verification, log access
- Impact: Need gateway security layer

Thought 5/7: Refresh strategy (adjusted)
Access: 15 min (client memory). Refresh: 7 days, rotate on use (HttpOnly cookie + DB revocation).

Thought 6/7: Gateway flow
1. Verify JWT signature 2. Extract tenant ID
3. Verify user belongs to tenant (cache + DB) 4. Forward with verified context

Thought 7/7 [FINAL]: Complete solution
JWT with refresh rotation + tenant ID + gateway verification.
15-min access, 7-day refresh. HttpOnly cookies + revocation DB.
Gateway enforces isolation. Confidence: High.
```
