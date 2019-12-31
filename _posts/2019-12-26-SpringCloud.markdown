---  
layout:     post  
title:      "SpringCloud开发记录"  
subtitle:   "SpringCloud"  
date:       2019-12-26 20:32:10    
author:     "cpuRick"  
header-img: "img/post-bg-2015.jpg"  
tags:  
    - GDAL  
---    
  

#  SpringCloud学习记录

## 版本选择
SpringBoot用来开发单个微服务，SpringCloud将整个微服务整合在一起。SpringCloud整个项目包含多个子项目，分为不同
的模块，整个微服务框架也包含很多不同的部分。各个部分担负不同的使命，一起构成了整个微服务系统。其中主要的
模块如下：
- 注册中心：Eureka 
- 配置中心：Config
- 客户端负载均衡：Ribbon
- 声明式Rest调用：Feign
- 服务容错：Hystrix
- 服务网关：Zuul
- 微服务跟踪：Spring Cloud Sleuth 

SpringCloud 版本发布的时候，会先发布一个Release版本，在Release版本发布之后，会发布该版本的SR版本，这个版本的意思是怼Release版本
bug的修改，SR来源于英文Service Release ,而每次Spring 版本发布的名称以伦敦地铁站的名称来进行命名，而且按照英文字母的先后顺序来保持
版本的迭代顺序。   
SpringBoot用来开发单体应用，但是如果单体应用要注册到整个微服务框架中去，就需要和SpringCloud相互协调，因此，二者的版本必须相互匹配。
[SpringCloud版本查看](https://spring.io/projects/spring-cloud)   
![SpringCloud版本](../img/SpringCloud版本.png)
其中，注意BootVersion的版本，以及Release train contents 中各个组件的版本，二者要保持协调。






## 服务注册
### 1.Eureka注册问题
在使用Eureka 构建自己的服务注册中心的时，现在提供的依赖已经由 **spring-cloud-starter-eureka** 转换为**Spring Cloud Starter Netflix Eureka Server**
   
只需使用下面的代码    
```
@SpringBootApplication
  @EnableEurekaServer
  public class EurekaApplication {
  
      public static void main(String[] args) {
          SpringApplication.run(EurekaApplication.class, args);
      }
  }
```
再添加上依赖
```
   <?xml version="1.0" encoding="UTF-8"?>
   <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
       <modelVersion>4.0.0</modelVersion>
   
       <groupId>com.springboot.cloud</groupId>
       <artifactId>eureka-server</artifactId>
       <version>0.0.1-SNAPSHOT</version>
       <packaging>jar</packaging>
   
       <name>eureka-server</name>
       <description>Demo project for Spring Cloud Eureka</description>
       <properties>
           <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
           <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
           <java.version>1.8</java.version>
       </properties>
   
   
   
       <dependencies>
           <!-- https://mvnrepository.com/artifact/org.springframework.cloud/spring-cloud-starter-netflix-eureka-server -->
           <dependency>
               <groupId>org.springframework.cloud</groupId>
               <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
               <version>2.1.4.RELEASE</version>
           </dependency>
           <!-- https://mvnrepository.com/artifact/com.google.code.gson/gson -->
           <dependency>
               <groupId>com.google.code.gson</groupId>
               <artifactId>gson</artifactId>
               <version>2.8.6</version>
           </dependency>
   
           <dependency>
               <groupId>junit</groupId>
               <artifactId>junit</artifactId>
               <version>4.12</version>
               <scope>test</scope>
           </dependency>
       </dependencies>
   
       <build>
           <plugins>
               <!--docker镜像build插件-->
               <plugin>
                   <groupId>org.springframework.boot</groupId>
                   <artifactId>spring-boot-maven-plugin</artifactId>
                   <version>2.1.4.RELEASE</version>
                   <configuration>
                       <mainClass>com.springboot.cloud.EurekaApplication</mainClass>
                       <fork>true</fork>
                   </configuration>
                   <executions>
                       <execution>
                           <goals>
                               <goal>repackage</goal>
                           </goals>
                       </execution>
                   </executions>
               </plugin>
               <plugin>
                   <artifactId>maven-compiler-plugin</artifactId>
                   <version>3.8.1</version>
                   <configuration>
                       <source>${java.version}</source>
                       <target>${java.version}</target>
                       <encoding>UTF-8</encoding>
                   </configuration>
               </plugin>
               <plugin>
                   <groupId>com.spotify</groupId>
                   <artifactId>docker-maven-plugin</artifactId>
                   <version>1.0.0</version>
                   <configuration>
                       <!-- 注意imageName一定要是符合正则[a-z0-9-_.]的，否则构建不会成功 -->
                       <imageName>cike/${project.artifactId}</imageName>
                       <dockerDirectory>${project.basedir}/src/main/docker</dockerDirectory>
                       <rm>true</rm>
                       <resources>
                           <resource>
                               <targetPath>/</targetPath>
                               <directory>${project.build.directory}</directory>
                               <include>${project.build.finalName}.jar</include>
                           </resource>
                       </resources>
                   </configuration>
               </plugin>
           </plugins>
       </build>
   </project>
```

经过笔者测试，以上pom配置文件能够成功打包出注册中心服务，对应的**SpringBoot版本为2.1.4**，使用上述配置就可以构建起自己的服务注册中心了。


 