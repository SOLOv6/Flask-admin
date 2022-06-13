# SOLOv6 Admin Dashboard Overview

<p align="center">
  <img width="319" alt="image" src="https://user-images.githubusercontent.com/85675215/173171356-b5e4092b-ebc7-47b4-bd47-1ac989ee4275.png">
</p>

# INDEX

- [**Introduction**](#Introduction)
  - [Directory](#Directory)
  - [Project Flow](#Project-Flow)

<br>

- [**Admin Dashboard**](#Admin-Dashboard)
  - [Structure](#Structure)
  - [Usecase](#Usecase)
  - [DB ERD](#DB-ERD)
  - [Service Flow](#Service-Flow)

<br>

- [**Demos**](#Demos)

<br>

- [**Tech Stack**](#Tech-Stack)

<br>

# Introduction

**SOLO**(Socar Only Look Once)**v6** 팀은 2022.04.18 ~ 2022.06.08 까지 약 7주 간, **차량 파손 탐지 및 분류 시스템 Upccida** 프로젝트를 진행하였습니다.
<br>
<br>
**Upccida** 는 사용자가 차량을 대여하는 시점에 업로드하는 사진들로부터 **차량의 파손 유무** 및 **파손 종류 분류**, **파손 영역 검출** 등의 Task 를 수행하는 시스템으로,
<br>
웹을 통해 모델의 inference 결과를 Admin Dashboard 에서 관리자가 확인 및 검수하여 최종적으로 보유 차량에 대한 파손 이력 관리가 가능하도록 구현하였습니다.
<br>
<br>
**Upccida** 프로젝트의 전반적인 Overview 는 [여기](https://github.com/SOLOv6/solov6-overview)에서 확인이 가능하며, 아래에서는 Flask API 로 구현한 관리자 검수 시스템에 대해 소개합니다.
<br>
<br>

## Directory

### /project

<img width="118" alt="image" src="https://user-images.githubusercontent.com/85675215/173288622-93958118-e49f-4e75-b4d0-bc8e222fbb47.png">

**project** 폴더 내의 디렉터리 구조는 위와 같습니다.

- **\_\_init\_\_.py** : project 패키지의 실행파일로, Flask app 반환
- **apis** : API 패키지
- **configs.py** : CSRF Token, DB Link, Flask 환경 변수 및 설정 파일
- **form** : 관리자 화면의 사용자 인증을 위한 Login & Register Form
- **models** : DB Table 및 각 컬럼에 대한 Scheme 정의
- **routes** : Flask app 에 연결된 각각의 라우팅 경로
- **static** : CSS, JS, Favicon image 와 같은 정적 파일
- **templates** : 각각의 화면을 구성하는 template 파일

<br>

### /project/apis

<img width="117" alt="image" src="https://user-images.githubusercontent.com/85675215/173305362-765e0750-10ee-4dcd-821f-28d14af8309c.png">

<br>

### /project/form

<img width="119" alt="image" src="https://user-images.githubusercontent.com/85675215/173305579-70e6702d-4d7d-4f37-a7e3-26d4c0135970.png">

<br>

### /project/models

<img width="113" alt="image" src="https://user-images.githubusercontent.com/85675215/173306642-fbf9915a-6208-406d-85d7-8c5eed8e0809.png">

<br>

### /project/routes

<img width="138" alt="image" src="https://user-images.githubusercontent.com/85675215/173306895-12cda9b6-1a8a-484b-b146-74e4069c12ba.png">

<br>

### /project/static

<img width="76" alt="image" src="https://user-images.githubusercontent.com/85675215/173307041-b4adde7b-a1f3-4678-bbcf-09ea84d7390c.png">

<br>

### /project/templates

<img width="127" alt="image" src="https://user-images.githubusercontent.com/85675215/173307281-ce10878d-5668-4b6e-9bfc-a31b4486f8ba.png">

<br>
<br>

## Project Flow

<p align="center">
    <img width="971" alt="image" src="https://user-images.githubusercontent.com/85675215/173314826-894827f1-de72-4f20-b52c-219b556335e0.png">
</p>
