---  
layout:     post  
title:      "Elastic-job-cloud+Mesos开发记录"  
subtitle:   "Elastic-job-cloud+Mesos"  
date:       2019-12-26 20:32:10    
author:     "cpuRick"  
header-img: "img/post-bg-2015.jpg"  
tags:  
    - GDAL  
---    
  

#  Mesos
## 简介
Mesos是加州大学伯克利分校开源的一个分布式资源管理框架，提供分布式环境下的集群管理能力。简而言之，Mesos将多台计算机抽象成为一个庞大的超级计算机。在Mesos之上，你可以
像使用一台计算机一样使用庞大的计算机集群。在实践过程中，Mesos曾成功管理了十万+的集群环境，其优良的性能经过实践的论证，是一款优秀的分布式资源管理框架。
### Mesos和Yarn、Spark有什么联系
Mesos 最大的特点就是二层资源调度机制。在Mesos集群之上，我们如果要运行应用，我们的应用是跑在应用框架之上，比如一个spark作业，它就是跑在spark之上，而spark又跑在mesos之上。
二层资源调度意思就是，mesos通过offer机制向其master中注册的应用框架提供资源，它并不直接调度应用。而应用框架在拿到mesos提供的资源之后，它负责对应用进行调度。
这种架构所产生的效果就是，在mesos集群之上，我们可以运行多个不同的计算服务，比如spark服务，elastic-job-cloud服务。而通过mesos提供的接口，我们也能开发自己的服务框架。
### Mesos和K8S、Marathon
Mesos 在进程隔离方面提供了两种不同类型的解决方案，linux cgroup 和容器。但它自身并不提供容器的编排、管理工作，而云计算时代的到来，容器化成为一种流行的解决方案，为此，开发了
Marathon项目，来进行容器化管理的工作。
所以Mesos+ Marathon是对标google 提出的k8s ，作为一种容器化的解决方案。


## Ubuntu 18.1 编译安装Mesos 1.9
**编译安装参考链接**：https://medium.com/@adheeq/apache-mesos-installation-in-ubuntu-2a97c4a9bd5d   
### 说明
Mesos 提供两种安装方案
- 手动编译安装
- 发布包安装
最为快捷的安装方案肯定是发布包安装，如果是centos用户，那么首先采用第二种安装方案。但是该方案下，目前只提Ubuntu 16 和ubutu 14的安装指导，
而笔者用的是ubuntu 18.1,所以只能采用第二种安装方案。   
编译安装的步骤也很类似，bootstrap、configure、make、make instll。大致步骤就是这样，但是提醒一点，最开始笔者是git clone git hub上mesos的项目源码
来进行编译安装的，怎么也不成功，后面采用apache mesos 官网提供的1.9版本源码，下载之后，就编译安装成功了。
### 注意
具体的安装步骤参考以下链接或者官网，现在对安装过程中的注意点进行说明。
1. jdk的版本，官方指导下，要求再安装mesos之前，需要安装open-jdk-8依赖，第一次构建的时候，笔者使用oracle jdk 8来进行构建，最后失败。
所以，在安装之前，建议安装open-jdk。如果存在java多个版本的管理问题，建议使用 update-alternatives 来对版本进行管理，具体使用方法可以百度。
2. Python版本，官方指导要求，安装之前,Python版本必须为2.7+，笔者最开始使用的python 版本是3.7。后面编译失败，所以建议,安装python 2.7版本。
3. 中文路径问题，建议编译路径中不要存在中文。
4. 编译过程很耗费时间，在make 中建议使用 -j 参数，来增加内核，提高编译速度。

## Mesos 1.9 本地集群搭建
###准备工作
#### 1.创建mesos工作目录
```shell script
mkdir /var/lib/mesos/master
mkdir /var/lib/mesos/slava
```
#### 2.搭建zookeeper服务
mesos中使用zk作为一致性存储，framework注册到mesos master中也必须通过zk。所以，在搭建mesos集群之前，我们要先有zk服务。
因为是本机测试，所以暂时采用 docker 搭建zk的单机服务。后面实际部署时，可采用高可靠性的zk集群。
```shell script
docker pull zookeeper
docker run -p  2181:2181 imageid
```
### 搭建集群
#### 1. master服务启动
采用**nohup**与**输入输出**重定向的方式来启动服务，可参考一下命令。
--quorum 参数表示，集群主备选举的时候，同意的最小数目，不可缺失。

```shell script
nohup ./bin/mesos-master.sh --ip=127.0.0.1 --work_dir=/var/lib/mesos/master  --quorum=1 --zk=zk://localhost:2181/mesos >./bin/mesos-master.log 2>&1 &
```
#### 2. slava服务启动
```shell script
nohup ./bin/mesos-agent.sh --master=127.0.0.1:5050 --work_dir=/var/lib/mesos/slave >./bin/mesos-slave.log 2>&1 &
```


# Elastic-job-cloud
## Elastic-job-cloud 简介
elastic-job 是当当网开源的项目，包含elastic-job-lite和elastic-job-cloud两个子项目，分别适用于单机环境和云化环境下，
二者采用统一的编程接口，一次开发，可在不修改代码的情况下由lite迁移到cloud中。    
elastic-job 定位为**分布式任务调度框架**，主要用于分布式环境下任务的分片、调度。同类型的框架大致如下：
- xxx-job:个人开源，轻量级任务调度框架
- LTS ：阿里员工个人开源项目
- Scheduler x  2.0 阿里最近开源的任务调度框架
- saturn 唯品会团队基于 elastic-job 1.0 开发的任务调度框架
 

elastic-job-cloud 基于mesos开发，从mesos的角度出发，其就是类似marathon之类的应用框架。

## Elastic-job-cloud 编译过程、搭建
- git clone 下载elastic-job的项目源码
- elastic-job项目采用了Lombok技术开发。在idea中，如果要编译源码，首先要安装 Lombok插件。
  在笔者编译过程中，分别在子项目顶层文件夹下运行 ```mvn -e compile```或者```mvn -e install```命令，来完成构建。

## 运行分布式作业 Elastic-job-cloud-example
在运行作业之前，首先我们要先运行elastic-job-cloud-scheduler 服务
- 首先修改conf文件夹下的配置文件
- 然后调用bin文件夹下start.sh 脚本文件
- 打开 http://localhost:8899/# 链接后，就能看见elastic-job的控制台了。

 
