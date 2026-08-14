# MOS Alpha-10E — Evolving Claim Timeline

Emergency balances change as rescue teams identify victims and authorities consolidate reports. MOS must preserve every version instead of overwriting history.

## Relations
- `INITIAL`: first observed version.
- `UPDATE`: only when the newer claim explicitly supersedes the previous claim.
- `CORRECTION`: only when the source explicitly identifies the previous value as erroneous.
- `DUPLICATE`: same value, same claim key.
- `UNRESOLVED_CHANGE`: values differ but no explicit relationship is established.

## Safety rule
A later timestamp alone does **not** prove that a value supersedes an earlier value. Until the relationship is established, MOS keeps both claims visible to the review layer.

## Example
`281 -> 285` may be an update, but MOS must not infer that merely because 285 is newer. The source/document must establish the relationship or the claim remains `UNRESOLVED_CHANGE`.
