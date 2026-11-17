---
name: lingbot-depth-integration
description: "LingBot-Depth 深度补全:depth_lab 独立项目+GPU(4070Ti显卡坞)0.2s/帧,验证方法与集成决策"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3b3c2ffb-3491-481e-806f-7972f645dc03
  modified: 2026-07-21T11:26:34.428Z
---

LingBot-Depth (深度补全, MDM/ViT-L) 于 2026-07-21 部署为**独立项目 `D:\Destop\depth_lab\`**(用户明确要求独立于 robot_code):

- 结构: `depth_lab\lingbot-depth\`(库+ckpt/model.pt 1.2GB) + `infer.py`(--device auto/cpu/cuda, --fp16, --repeat)
- 环境: conda env **lingbot-gpu** (D:\miniconda\envs\lingbot-gpu, py3.10, torch 2.6.0+cu124, xformers 0.0.29.post2, mdm -e)
- GPU: RTX 4070 Ti 12GB 经 USB4 显卡坞(联想82RC笔记本)。驱动须用 NVIDIA 官网完整版(610.74,统一管 3050 Laptop+4070 Ti);OEM笔记本驱动不含桌面卡INF会报代码31。装驱动前须清掉 Windows Update 的 pending reboot
- **实测速度(box_1帧 1280x720)**: GPU PyTorch 稳态 0.195s/帧(infer内部已是bf16 autocast+xformers) vs CPU 828s;**TensorRT fp16 引擎 110ms纯推理/120ms端到端**(vs PyTorch 差1.46mm中位,mask 100%一致)
- TRT 部署链(depth_lab): export_onnx.py(forward为导出边界,num_tokens=3600静态) → fp16转换+手术(onnx/model_fp16_trt.onnx) → trt_build.py(引擎 onnx/model_fp16.engine 650MB,构建107s,绑定4070Ti不可移植)。**踩坑清单**: ①`|=`就地操作不可导出(mask_utils.py已改) ②ORT优化器BiasGelu私有算子TRT不认(须从原始fp32转) ③fp16转换器漏Resize输出Cast和121个Cast(to=fp32)节点(脚本统一翻转) ④TRT11删除FP16 flag/EXPLICIT_BATCH,精度由ONNX图类型决定 ⑤ORT路线死刑:注意力融合不匹配反而慢6倍(1240ms)
- robot_code 侧只保留 `tools/capture_rgbd_frame.py`;两项目靠 captures/ 目录文件格式(rgb.png/raw_depth.png 16bit mm/intrinsics.txt)交换,零 import
- 集成决策: **暂不进主工程**。待物理层改造(哑光台面+漫射光)后测无效率,仍>3%才按"本地服务+薄客户端(降级到原始深度)"模式集成
- 可信度结论(平面拟合验证法,RANSAC台面/盒面平面做基准): 台面/盒面等平坦区域补全误差中位3-5mm(与传感器噪声同级);盒高误差±4mm;**盒边缘±10px不可信**(阶跃保留率最差18%,跨边缘洞误差~20mm),轮廓必须用RGB分割
- CPU 跑法(备用): mmap=True+assign=True 加载(16GB内存机器整读会0xC0000005崩溃);block.py 有无xformers等价回退补丁
- 大文件下载经验: pip 无断点续传,国内下 torch 用 curl -C - 单连接+重试从 mirrors.aliyun.com/pytorch-wheels;并发分段会触发阿里云限速
- Windows 控制台需 PYTHONUTF8=1
- v2.0(2026-07发布)不开源:1.5亿样本(v0.5为1000万),镜面/玻璃场景RMSE减半,Orbbec将出 Gemini330系列边缘SDK(年底集成相机),届时可替换后端

相关: [[l6-path-optimization-method]] [[storage-rollout-next-tasks]]
