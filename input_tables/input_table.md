| name        | type   | hosts | in_port | in_device | out_device | out_port |
| ----------- | ------ | ----- | ------- | --------- | ---------- | -------- |
| KL          | switch | 80    |         |           | KL         | Fa0/0    |
| Penang      | switch | 52    |         |           | Penang     | Fa0/0    |
| JB-wireless | switch | 50    |         |           | JB-switch  | Fa1/1    |
| JB          | switch | 18    |         |           | JB         | Fa0/0    |
| Offsite-LAN | switch | 8     |         |           | KL         | Fa0/0    |
| JB-P        | router | 2     | Se3/0   | JB        | P          | Se3/0    |
| P-KL        | router | 2     | Se2/0   | P         | KL         | Se2/0    |
