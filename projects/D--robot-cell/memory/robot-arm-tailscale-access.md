---
name: robot-arm-tailscale-access
description: 通过 Tailscale 子网路由从 Mac 远程访问机械臂 Web 界面的网络配置
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1825356b-dd6b-48af-b126-317b1df5fe63
---

机械臂 Web 控制界面在 `http://192.168.0.20:7000/`(服务器是 WebSocket++,实时控制走 WebSocket）。机械臂通过网线接在一台 Windows 电脑上,Mac 通过 Tailscale 子网路由远程访问,两台不在同一网络。

**Tailnet**(账号 liangchen98ag@gmail.com,域 `tail7f7e40.ts.net`):
- **blue-space** = Windows 11,Tailscale IP `100.106.76.91`,作为**子网路由器**,广播 `192.168.0.0/24`。它连机械臂的以太网卡 IP 是 `192.168.0.10/24`,靠 WiFi(192.168.31.x)上网。已在 Windows 上设 `IPEnableRouter=1` + `tailscale set --advertise-routes=192.168.0.0/24`,后台已批准该路由。
- **chenmacbook-air** = Mac,Tailscale IP `100.67.85.97`,已 `RouteAll: true`(接受子网路由),`192.168.0.0/24` 经 `utun7` 走 Tailscale。

**能访问的前提**:Windows 开机 + Tailscale 运行 + 网线连着机械臂;Mac 的 Tailscale 也开着。

**排查要点**:
- ping `192.168.0.20` 超时是正常的(机械臂不回 ICMP),用 `nc -vz 192.168.0.20 7000` 或 `curl -I http://192.168.0.20:7000/` 测端口才准。
- Mac 本地路由表有条 `192.168.0/16 → 192.168.31.1`(本地网关),但 Tailscale 装的 `192.168.0.0/24` 更具体,最长前缀匹配会优先走隧道,正常。
- blue-space 默认约 180 天密钥过期会导致中转失效;建议在后台 Disable key expiry。

相关:[[ros2-foxglove-setup]] [[sim-as-validation-platform]]
