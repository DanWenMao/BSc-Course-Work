# README

## Workflow

1. 下载火震数据

​	[InSight Notebook - Mars Lander data](https://an.rsl.wustl.edu/ins/an/an3.aspx)

​	找到Sol 1094，仪器SE，选择数据，加入chart，在chart中提交申请，数据打包发送至邮箱（天地良心）

2. 寻找合适的数据

   下载的数据包括csv（给人看的）和mseed（真正的地震波记录）

   mseed文件命名规则为：Network.DataType.Location.Channel.Year.DOY.Segment.mseed

   - Network：地震台网，=XB，代表InSight SEIS网络
   - DataType
     - elyh0: 原始数据
     - elyso: 派生数据？
     - elyse: SEIS科学级数据，已去除仪器相应和温度/工程影响
     - elyhk: HouseKeeping，记录仪器运行状态，可以用于解释噪声来源
   - Location：传感器类型+数据处理路径
     - 00: Short Period
     - 02: Very Broad Band
     - 03: VBB辅助/派生
     - 05: 温度/辅助
     - 65: 工程转换数据，中间产品
     - 68: Short Period（处理后）
     - 85: Very Short Period
   - Channel: band instrument component
     - Very Broad Band: bhu, bhv, bhw
     - Short Period: shu, shv, shw
   - Year.DOY
   - Segment

3. 去仪器相应

4. 选择垂直分量

5. 滤波

Onodera, K. (2023), Sample program for analyzing the InSight seismic data, Zenodo, doi:10.5281/zenodo.7927454.