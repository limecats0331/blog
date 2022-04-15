---
title: "vue-express 연동하기 2022"
description: 'vue-express 연동 삽질기'
date: 2022-03-28T04:46:25+09:00
tags : ["Vue","express"]
categories: "study"
comments: true
draft: false
---

## 들어가기앞서

2022년 3월 이제 뭔가 만들어볼 수 있겠다! 싶었다. 그래서 지금까지 배운 `vue`와 `express`를 연동해서 뭔가 만들어보고 공부해보자 라는 생각으로 연동을 시작했다.

당연히 구글 검색을 통해서 연동을 시도했는데 빌드부터 오류를 뱉거나 `api`호출이 안되는 경우가 생겼다. 찾아보니 지금 검색해서 나오는 글이 2년에서 4년전 글이여서 `Vue`의 버전이 다른게 컸다. 그래서 2022년도 지금 기준으로 최신 버전인 `Vue 3.x`에 맞게 글을 쓰고자 한다.

## Vue-node 연동하기

### 환경

이 글은

`Vue CLI v5.0.4`

`Vue 3.x`

을 기준으로 작성되었다.

### Vue

원하는 폴더에서

```console
vue create frontend
```

를 통해서 `vue` 프로젝트를 생성해준다. 여기서 중요한 것은 `vue-router`를 같이 설치해주는 것이다. 그러면 다음과 같이 프로젝트가 생성된다.

```console
├── README.md
├── babel.config.js
├── jsconfig.json
├── node_modules
├── package-lock.json
├── package.json
├── public
│   ├── favicon.ico
│   └── index.html
├── src
│   ├── App.vue
│   ├── assets
│   ├── components
│   ├── main.js
│   ├── router
│   ├── store
│   └── views
└── vue.config.js
```

우리는 백엔드 서버를 통해서 build한 결과물을 보여줄 것이다. 그러기 위해서 `vue.config.js` 파일을 열어서 build 위치를 변경해야된다.

> `vue.config.js`
>```js
>const { defineConfig } = require('@vue/cli-service')
>const path = require('path')
>module.exports = defineConfig({
>   transpileDependencies: true,
>
>   //build dir를 외부로 빼줌
>   outputDir : path.resolve(__dirname,'../backend/public')
>})
>```

vue.config.js에 들어갈 수 있는 option들에 관련된 정보는 [여기](https://next.cli.vuejs.org/config/#vue-config-js)에서 확인할 수 있다.

이러면 `Vue`에서의 준비는 끝!

### express

솔직히 `express`는 별로 바뀐게 없어서 크게 다른 점이 없었다. `express-generator`가 설치되지 않았다면 설치하고 `express`를 설치해주면 된다.

```console
npm install express-generator -g
express backend --view=pug
```

그리고 우리는 view에 관련된 부분을 `Vue`를 사용할 것이기 때문에 `app.js`를 열어서 view에 관련된 부분을 삭제시켜준다.

>app.js
>```js
>// view engine setup //이 부분을 삭제
>app.set('views', path.join(__dirname, 'views'));
>app.set('view engine', 'pug');
>```

그리고 `'/backend/views'` 폴더도 삭제시켜주자!

#### 404문제 해결

여기서 Vue를 통해서 SPA를 만들었기 때문에 몇가지 문제가 발생한다. 바로 라우팅 문제인데 만약 `/login` 페이지에 접속했다고 생각해보자. 여기서 새로고침을 누르게 되면 서버는 `'/login'`으로 `GET`요청을 보내게 된다. 하지만 우리는 `Vue`에서 페이지에 대한 라우팅을 처리하고 있기 때문에 서버는 `404`오류를 뱉게 된다.

이문제를 해결하기 위해서 2가지 옵션이 있다.

##### 1. `connect-history-api-fallback`
첫째는 `routes/index.js`를 열어서 다음과 같이 수정해준다.

> `index.js`
>```js
>var express = require('express');
>var router = express.Router();
>var path = require('path')
>
>/* GET home page. */
>router.get('/', function(req, res, next) {
>  res.sendFile(path.join(__dirname,'../public','index.html'));
>});
>
>module.exports = router;
>```

이러면 서버에 접속하면 `index.html`파일을 보내주게 된다. 그후에 `connect-history-api-fallback`이라는 미들웨어를 설치해준다. 자세한 것은 [깃허브](https://github.com/bripkens/connect-history-api-fallback)에서 확인할 수 있다.

```console
npm install connect-history-api-fallback
```

그리고 `/backend`의 `app.js`에 다음과 같이 추가해준다.

>`app.js`
>```js
>var history = require('connect-history-api-fallback');
>app.use(history());
>app.use(express.static(path.join(__dirname, 'public')));
>```

여기서 `app.use(history());`의 위치가 중요한대 `app.use(express.static(path.join(__dirname, 'public')));` 보다 위에 있어야 된다고 한다.

이러면 `express` 설정도 끝!

##### 2. `get('*',[callback])`
두번째 방법은 조금 더 쉬운 방법이다. `routes/index.js`를 열어서 다음과 같이 수정해준다.

> `index.js`
>```js
>var express = require('express');
>var router = express.Router();
>var path = require('path')
>
>/* GET index.html */
>router.get('*', function(req, res, next) {
>  res.sendFile(path.join(__dirname,'../public','index.html'));
>});
>
>module.exports = router;
>```

이러면 끝이다. 그러면 모든 라우팅에 대해서 `index.html`을 호출하고 vue-router에서 설정한 대로 라우팅하게 된다. 여기서 주의할 점이 있는데 이렇게 되면 API call도 모두 `index.html`을 호출하게 될 수 있다.

그래서 `/backend`의 `app.js`에 다음과 같은 순서로 라우팅해준다.

>`app.js`
>```js
>app.use('/api',apiRouter);
>app.use('/', indexRouter);
>```

`Node.js`의 미들웨어는 위에서부터 실행되기 때문에 `'/api'`로 들어가는 호출은 한번 걸러지고 남은 호출은 모두 `index.html`을 호출하게 된다. 추가로 API를 나누고 싶으면 `app.use('/', indexRouter);` 위에 선언해주면 된다.

> 두 방식이 어떤 차이점이 있고 두번째 방식을 사용하는 사람들이 없던데 어떤 단점이 있는지 잘 모르겠다. 아시는 분은 댓글 남겨주세요..!

### build & start

이제 아까 만들었던 `'/front'`폴더로 들어가서 빌드를 해준다.

```console
npm run build
```

그리고 `'/backend'` 폴더로 가서 서버를 실행해주면 끝이다.

```console
npm start
```

이제 `http://localhost:3000/` 로 접속하면 빌드한 `vue`파일을 볼 수 있다. 또한 routing한 페이지도 잘 보이고 새로고침해도 `404` 오류가 나지 않는 것을 볼 수 있다.
