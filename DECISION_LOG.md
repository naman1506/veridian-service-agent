# Decision log

Generated from the no-key deterministic run on the frozen clock, Friday 25 September 2026, 17:00 IST.

| Case | Decision | Rationale | Citations |
| --- | --- | --- | --- |
| REQ-01 | ROUTE_TO_HUMAN | 3.5 years triggers a KB-03 / asset-policy conflict | KB-03, ASSET-POLICY, TK-1043 |
| REQ-02 | AUTO_RESOLVE | Guest Wi-Fi is kiosk self-service for 24 hours | KB-07, TK-1051 |
| REQ-03 | AUTO_RESOLVE | Six failed attempts require manual unlock | KB-01 |
| REQ-04 | MONITOR | Security review remains within 3-5 business days | KB-04, TK-1044 |
| REQ-05 | AUTO_RESOLVE | Employee renews expired VPN credentials | KB-02, TK-1042 |
| REQ-06 | NEEDS_INFO | Need queue check, spooler restart, and asset tag | KB-05 |
| REQ-07 | ROUTE_TO_HUMAN | Manager and Finance approvals precede shipping | KB-10, TK-1047 |
| REQ-08 | FLAG_RISK | Forwarding suspected phishing is an active violation | KB-09, TK-1048 |
| REQ-09 | AUTO_RESOLVE | Archive now; manager approves any quota increase | KB-06, TK-1045 |
| REQ-10 | ROUTE_TO_HUMAN | No policy covers finance-server admin access | TK-1050 |
| REQ-11 | NEEDS_INFO | Contractor VPN requires manager form | KB-02 |
| REQ-12 | NEEDS_INFO | Finance owns provisioning; confirm account exists | KB-08 |
| REQ-13 | AUTO_RESOLVE | Two-year device goes to repair, not replacement | KB-03, ASSET-POLICY |
| REQ-14 | AUTO_RESOLVE | Non-catalog browser extension enters Security review | KB-04 |
| REQ-15 | NEEDS_INFO | Request lacks a routable symptom | Guarded low confidence |
| TK-1043 | MONITOR | Approved replacement awaits IT fulfilment | TK-1043 |
| TK-1044 | MONITOR | Security review stays in SLA | KB-04, TK-1044 |
| TK-1047 | MONITOR | Finance owns the pending home-office approval | KB-10, TK-1047 |
| TK-1048 | MONITOR | Security owns active phishing investigation | KB-09, TK-1048 |
