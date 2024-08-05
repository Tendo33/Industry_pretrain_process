# 采空区瓦斯流动规律的CFD模拟  

胡千庭1,2,3，梁运培²,3，刘见中4  

（1．中国矿业大学（北京）资源与安全工程学院，北京100083；2．山东科技大学资源与环境工程学院，山东青岛266510；3．煤炭科学研究总院重庆分院瓦斯研究所，重庆400037；4．煤炭科学研究总院科技发展部，北京100013)  

摘要：采用CFD数值模拟方法对采空区瓦斯流动及分布规律进行了研究．阐明了计算流体力学CFD模拟的理论基础，介绍了运用FLUENT程序开发CFD模型的方法，并运用所开发的CFD模型对张北矿11418工作面采空区瓦斯流动规律以及地面钻孔抽放条件下瓦斯流动规律进行了模拟，模拟结果表明：采空区回风巷侧的最大瓦斯浓度可达$80\%$．同时表明：采用CFD模型研究采空区瓦斯流动规律是可行的方法之一.  

关键词：采空区流场；瓦斯流动规律；CFD 模拟  

# CFD simulation of goaf gas flow patterns  

HU Qian-ting1,23 , LIANG Yun-pei2,3 , LIU Jian-zhong  

(1. School of Resource and Safety Engineering,China University of Mining and Technology (Beijing），Beijing 100083,China; 2. College of Natural Resource and Environmental Engineering, Shandong University of Science and Technology, Qinagdao 266510, China; 3. Gas Department Chongqing Branch, China Coal Research Institute, Chongqing 400037,China; 4. Dept. of Science and Technology,China Coal Research Institute, Beijing 100013，China)  

Abstract: Goaf gas flow and distribution patterns were studied by means of CFD numerical simulation. Discussed the theoretical basis of computational fluid dynamics ( CFD） simulation, and introduced the CFD model develop- ment method based on FLUENT program. Goaf gas flow patterns, as well as gas flow rules by boreholes drainage , were simulated applying the developed CFD model at Panel 11418 of Zhangbei coal mine. The simulating results show that the maximum gas concentration can be $80\%$  at the side of return airways. It suggests that studying goaf gas flow patterns applying CFD model is one of the feasible methods.  

Key words: flow field in goaf; gas flow patterns; CFD simulation  

掌握采空区瓦斯分布和流动规律，是研究工作面合理通风方式、防治自然发火以及瓦斯治理的关键的技术基础[1\~3]．为了研究采空区瓦斯流动规律，笔者在张北矿11418 工作面采用束管监测系统测定采空区气体的分布，同时采用基本CFD（计算流体力学）模型对采空区瓦斯流动规律进行了数值模拟．本文主要介绍运用CFD模型模拟采空区瓦斯流动及分布规律的方法和结果.  

# 1采空区瓦斯流动及分布的CFD模拟方法  

采空区瓦斯流动非常复杂，它受多种因素的影响，如通风、瓦斯密度、浮力，以及采空区渗透性．进行CFD数值模拟是为了深人了解采空区瓦斯流动及分布规律，  

# 1.1采空区瓦斯流动CFD模拟的理论基础  

CFD模拟研究是为了得到流体流动控制方程的数值解法，它通过时空求解得到所关注的整体流场的数学描述[4.5]．CFD 的基础是建立 Navier－Stokes 方程，它是由一系列描述流体流动守恒定律的偏微分方程组成的．为了模拟采空区混和气体在工作面后方的运移，模型必须像对一种气体的守恒方程那样，对质量和动量的守恒方程进行求解．质量守恒方程或称连续性方程，可表示为  

$$
\frac{\partial\rho}{\partial t}\,+\,\nabla\,\cdot\,\left(\rho\pmb{\nu}\right)\;=\;S_{{\scriptscriptstyle m}}\,,
$$  

式中，$\rho$为密度；$t$为时间；$v$为速度；源$S_{m}$为从分散次生相和任何其它用户自定义的源加在连续相上的质量.  

式（1）是质量守恒方程的常规形式，它对不可压缩流体和和压缩流体都适用动量守恒方程在一个惯性参照系（没加速度）内可表示为  

$$
\frac{\partial}{\partial t}(\rho\pmb{\nu})\ +\ \nabla\,\cdot\,(\rho\pmb{\nu}\pmb{\nu})\ =-\ \nabla\,p\ +\ \nabla\,\cdot\,(\pmb{\tau})\ +\rho\pmb{g}\,+\pmb{F}\,,
$$  

其中，$p$为静压力；$\pmb{\tau}$为应力张量；$\rho\pmb{g}$和$\pmb{F}$分别为重力体力和外部体力．$\pmb{F}$同样包含其它的附属于模型的源，如多相介质和用户自定义源  

在研究中，采空区被看作是多孔介质，相对于标准的流体流动方程，附加了动量源进行模拟．此源由2部分组成：黏滞损失项（式（2）右首第1项）和惯性损失项（式（2）右首第2项).  

$$
S_{i}\ =\ \sum_{j\,=\,1}^{3}D_{i j}\mu v_{j}\,+\,\sum_{j\,=\,1}^{3}C_{i j}\,\frac{1}{2}\rho v_{\mathrm{mag}}v_{j}\,,
$$  

式中，$S_{i}$为第$i$个$(\,x\,,~y$或$z$）动量方程的源;$\mu$为分子黏度；$\pmb{D}$和$c$为预定义的矩阵；$v_{\mathrm{mag}}$为速度向量的模；$v_{j}$为在$x$，$y$和$z$方向的速度分量，该动量的减弱将有利于孔隙单元中压力梯度的产生，所引起的压力降与单元中的流动速度（或速度平方）成比例.  

在多孔介质层流中，压力降一般与速度成比例．忽略对流加速度和扩散，可用 Darcy 定律简化多孔介质模型，即  

$$
\nabla_{\displaystyle{p}}\,=\,-\,\frac{\mu}{\alpha}\nu\,,
$$  

式中，$\alpha$为渗透率.  

在孔隙区域3个坐标轴$\left(\,x\,,\,\,y\,,\,\,z\,\right)$方向的压力降为  

$$
\Delta p_{x}\ =\ \sum_{j\,=\,1}^{3}\ \frac{\mu}{\alpha_{x_{j}}}v_{j}\Delta n_{x}\,,\ \Delta p_{y}\ =\ \sum_{j\,=\,1}^{3}\ \frac{\mu}{\alpha_{y_{j}}}v_{j}\Delta n_{y}\,,\ \Delta p_{z}\ =\ \sum_{j\,=\,1}^{3}\ \frac{\mu}{\alpha_{z_{j}}}v_{j}\Delta n_{z}\,,
$$  

式中，$1/\alpha_{i j}$为矩阵$\pmb{D}$中的项；$\Delta n_{x}$，$\Delta n_{y}$和$\Delta n_{z}$为孔隙区域在$x$，$y$和$z$方向的厚度.  

采空区气体运移的主控因素有：由于浓度、热梯度造成的分子扩散，以及由于压力梯度造成的黏性流或质量流．根据Fick定律，扩散的发生如下，即  

$$
J_{i}\,\,=\rho D_{i m}\,\frac{\partial X_{i}}{\partial x_{i}}-\frac{D_{i}^{T}}{T}\,\frac{\partial T}{\partial x_{i}},
$$  

式中，$J_{i}$为第$i$种气体的扩散流量，它是由浓度梯度、热梯度引起的；$D_{i m}$为混和气体的扩散系数；$X_{i}$为气体 $i$ 的质量分数； $D_{i}^{T}$ 为热扩散系数； $T$ 为温度.  

对于非稀薄气体，式（3）可用多组分的扩散公式代替，即  

$$
J_{i}\,\,=\rho\,\frac{M_{i}}{M_{\mathrm{mix}}}\sum_{j,\ j\neq i}D_{i j}\biggl(\frac{\partial X_{j}}{\partial x_{i}}+\frac{X_{j}}{M_{\mathrm{mix}}}\,\frac{\partial M_{\mathrm{mix}}}{\partial x_{i}}\biggr)-\frac{D_{i}^{T}}{T}\,\frac{\partial T}{\partial x_{i}},
$$  

式中，$M_{i}$为气体$i$的分子量；$M_{\mathrm{mix}}$为混合气体的分子量；$\pmb{D}_{i j}$是气体$j$中气体组分$i$的多组分扩散系数.以上分析了建立采空区气体流动模型的基本方程及其原理，在确定模型的边界条件后，可以运用数值解法求其解析解，即可得到采空区瓦斯流动及分布规律  

# 1.2采空区瓦斯运移模拟CFD模型开发  

基于上述原理，采用商业的CFD 程序FLUENT来模拟采空区气体的流动规律I6]．FLUENT是通过有 限体积的流体动力学计算，来求解Navier-Stokes方程．为了得到采空区瓦斯流动规律的典型情况，将三维CFD模型划分大约500000个单元格．CFD模型是通过FLUENT的Gambit前处理器进行构建和划分网格的，随之导人解算器进行模拟．三维的FLUENT模型可包含四面体、六面体、棱锥体、楔形单元或它们的组合．本次开发的CFD模型的一个创新点，是通过一系列与求解器连接的用户自定义函数，将采空区渗透率分布和瓦斯涌出相结合．这些用户自定义函数采用C语言编写，被解释和编译后用图形用户面板与FLUENT的求解器连接  

煤岩层的渗透率是控制工作面瓦斯涌出的主要因素．由开采引起的应力分布对开采层和邻近层的渗透率都有影响，从而就决定了瓦斯涌出规律．渗透率的递减量取决于工作面前方地层的裂隙发育程度，以及工作面后方的应力释放程度．不同的岩石，由于其开采层强度和孔隙率的不同，其渗透率的变化也不同.通过对采空区应力载荷分布规律的分析及以前CFD模拟研究的经验，确定了采空区的渗透率分布，不同区域的渗透率变化为$10^{\textrm{-4}}\!\sim\!10^{\textrm{-9}}\textrm{m}^{2}$．采空区最大黏性渗透率约为$10^{\ -10}\ \mathrm{m}^{2}$  

采空区被看作多孔块体，并用已编写好的外部子程序对在此区域内的孔隙率和采空区气体（作为一个质量源）的连续分布进行定义．这些“源”随后被加人“通过多孔介质流动”的基本子程序模块．在这些子程序模块中，混和气体通过多孔的采空区的流动，是通过在动量方程上添加一个动量水槽来模拟的，该水槽的黏性部分与黏度成正比，而惯性分量与气体的动能成正比．通过该子程序来反映不同的通风和采空区瓦斯涌出情况，这些子程序随后被组合到CFD主程序以进行模拟.  

对于此研究，由于标准的$\kappa-\varepsilon$方程($\kappa$为湍动能，$\varepsilon$为耗散率）模拟大范围湍流流动的功能更加强大、高效，且具有合理的精度，因此用它来模拟气体在采空区的湍流．这种最简单的湍流“全模型”包括2个公式，这2个相互分离的传送公式的求解，允许湍流速度和长度的比例各自独立确定．用该模型可模拟近工作面的湍流流动和采空区内部的层流流动.  

# 1.3采空区瓦斯运移规律CFD模拟的方法  

采空区内的气体流动规律是复杂的，它涉及多种因素，如通风、气体密度、浮力和采空区渗透性．综 合考虑这些因素，并结合试验工作面的具体情况，建立了CFD模型，并通过模拟建立了基本的采空区分布形态．模型应用了现场收集的数据，以及以往采空区瓦斯流动CFD建模的经验，  

CFD 模型的建立主要包括以下工作:  

（1）现场收集工作面采空区的几何形状和其它参数，如瓦斯流量和采空区垮落特征等（3）通过用户自定义子程序设置流动模型和边界条件.（4）工作面基本情况模型的模拟（5）用现场测量的采空区瓦斯监测和抽放数据对基本模型进行校准和验证，用这些信息，建立一组三维的CFD模型，以模拟采空区瓦斯的分布特征.  

# 2张北矿11418工作面采空区瓦斯分布规律的CFD模拟  

# 2.111418工作面采空区瓦斯浓度监测  

为了现场测定采空区瓦斯分布规律，采用改进的采空区气体监测方案，并布置了束管监测系统，对采空区气体浓度进行了监测．图1为14118工作面从开切眼推过$350\,\mathrm{~m~}$后，工作面后方风巷侧的采空区管束监测点的气样分析结果．该结果表明，渗人采空区的氧气含量是非常高的，即便在工作面后方$100\textrm{m}$的风  

![](/workspace/sunjinfeng/github_projet/Industry_pretrain_process/data/test_data_output/69b35957d5252d728792e06f0ae6843f37cf01d89b2914052c9e90ccc606c913.jpg)  
图1张北矿11418 工作面采空区气体浓度分布曲线Fig. 1  The curves of goaf gas concentration distribution at Panel 11418 of Zhangbei coal mine  

巷侧采空区也是如此．采空区瓦斯在向采空区后方方向有增大的趋势.  

# 2.211418工作面采空区瓦斯分布规律CFD模拟  

图2为 11418 工作面 CFD 模型的几何特征.建模的基本参数如下：工作面走向长$580\,\mathrm{~m~}$，宽$180\,\mathrm{~m~}$，高$3.~0~\mathrm{m}$；巷道宽$4.~0\,\mathrm{~m~}$，高$3.\,0\,\mathrm{~m~}$； CFD模型顶部和底部高$100\,\mathrm{~m~}$，包括区段上方$65\,\mathrm{~m~}$和下方$35\,\mathrm{~m~}$；煤层倾斜，垂直工作面(推进)方向，沿工作面(推进)方向$3^{\circ}$，回风平巷在下部（运输平巷以下$12\textrm{m}$)，工作面水平高出开切眼$50\sim60\,\mathrm{~m~}$通风系统为“U”形通风，风量$2~600~\mathrm{m}^{3}/\mathrm{min}$；整个采空区瓦斯涌出量为$21.~0\sim\!24.~0~\mathrm{m}^{3}/\mathrm{min}$；气体组分为$100\%$$\mathrm{CH_{4}}$；采空区抽放钻孔和9－2号煤层的瓦斯抽放巷道为$6~\mathrm{m}^{2}$．基本模型采空区垮落带高$100\,\mathrm{~m~}$，底板岩层中包括下部的6 和7号煤层．基本模型中布置了3个地面采空区钻孔.  

图3为在开采层水平的采空区气体分布规律的 CFD 模拟．结果表明:采空区回风巷侧的最大瓦斯浓度可达$80\%$．进人采空区的氧气量是很高的，尤其是在工作面机巷侧；在工作面后方$300\,\mathrm{~m~}$处进风巷侧的氧气浓度可超过$12\%$，而回风巷侧工作面后方$150\,\mathrm{~m~}$处有氧气聚集，这与现场实测数据相吻合.  

![](/workspace/sunjinfeng/github_projet/Industry_pretrain_process/data/test_data_output/86c7b0255f3aac43edb0c2377bfab3704619bb894e5582ba0495249ac41c09a9.jpg)  
图211418 工作面基本的 CFD 模型几何特征 Fig. 2 The basic geometry of CFD model of Panel 11418  

![](/workspace/sunjinfeng/github_projet/Industry_pretrain_process/data/test_data_output/2f130289df9ee4866b21b9698f3124bf1f2a618898d36dc4c6296a8d7b69fc6c.jpg)  
图314118工作面采空区气体分布的CFD模拟Fig. 3  Goaf gas distribution in the CFD model of Panel 11418 抽放钻孔没打开  

# 311418工作面钻孔抽放条件下采空区瓦斯分布  

用CFD分别对多种不同的情况进行了模拟，以此分析地面钻孔抽放采空区气体的效果以及采空区气体分布规律．模拟研究中，在孔口施加$40\sim75~\mathrm{kPa}$的抽放负压．图4显示了在抽放和未抽放条件下采空区瓦斯分布的不同，在抽放条件下靠近工作面回风巷侧瓦斯向采空区深部运移．这说明了采空区地面钻孔抽放的作用，一方面在于抽出瓦斯，另一方面在于改变瓦斯的流向.  

由图3可以看出，采空区瓦斯分布和氧气分布呈对称关系，增减趋势相反，因此通过分析氧气分布规律可以考察瓦斯分布，同时对氧气分布进行考察，可以有效地控制采空区抽放条件下的自然发火现象，因此对不同钻孔组合情况下采空区氧气的分布规律进行了CFD模拟（图5）.  

由 CFD 模拟结果可以看出：  

（1）采空区钻孔在中等抽放负压（$.40\sim60\ \mathrm{kPa}$）下，在工作面推过钻孔后，可得到的瓦斯流量为 20  

![](/workspace/sunjinfeng/github_projet/Industry_pretrain_process/data/test_data_output/e31f3a5f2035d0d997c1422501426e689fafdc2c7c0bf54e7a2729d5c1cfd64e.jpg)  
图4抽放和未抽放条件下采空区瓦斯分布的对比Fig. 4 The comparision of goaf gas distribution under drainage or undrainage conditions  

$\sim\!40\,\mathrm{\m}^{3}/\mathrm{min}$，浓度为$80\%$；所抽得的氧气浓度为$2\%\sim\!7\%$，预计能维持一个稳定的抽放流量.  

（2）当2个钻孔同时工作时，将进入采空区和抽放系统更多的氧气．接近工作面的采空区钻孔所获得的采空区气体的氧气浓度将很 高.  

（3）将采空区钻孔靠近工作面布置，有利于控制上隅角瓦斯超限  

空区的瓦斯抽放钻孔，以提高整体的瓦斯抽放  

![](/workspace/sunjinfeng/github_projet/Industry_pretrain_process/data/test_data_output/50d277f97f8c27732d0d89e176a5d2209e584d95383879b0e57e743802b1866d.jpg)  
效果，并应对采空区深处的钻孔采取连续、中等流量抽放的方式  

# 4结论  

（1）现场实测瓦斯分布规律难度大、工程量大，且效果不理想．经对比研究，采用CFD模型模拟得到的采空区瓦斯流动规律与现场实测结果相吻合．因此，采用CFD模型研究采空区瓦斯流动规律是可行的方法之一。  

（2）CFD模拟结果表明，采空区回风巷侧的最大瓦斯浓度可达$80\%$，同时，进入采空区的氧气量很高，尤其是在工作面机巷侧.  

（3）采用CFD模型模拟了地面钻孔抽放条件下瓦斯流动规律，可为地面采空区的瓦斯抽放钻孔设计提供依据.  

# 参考文献:  

[1］梁运培，孙东玲．岩层移动的组合岩梁理论及其应用研究［J]．岩石力学与工程学报，2002，21（5）：654～657.

[2］许家林，孟广石．应用上覆岩层采动裂隙“0”形圈特征抽放采空区瓦斯［J]．煤矿安全，1995（7)：2～4.

[3］梁栋，周西华．回采工作面瓦斯运移规律的数值模拟［J]．辽宁工程技术大学学报，1999，18（4)：$337\sim341

$[4］王福军．计算流体动力学分析［M]．北京：清华大学出版社，2004.

[5］傅德薰，马延文．计算流体力学［M]．北京：高等教育出版社，2004.

[6]淮南矿业（集团）有限责任公司，煤炭科学研究总院重庆分院，澳大利亚联邦工业科学院．地面钻井抽放采动区域瓦斯技术研究[R]．重庆：2006.  