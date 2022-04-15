---
title: "js constructor와 prototype"
description:
date: 2022-04-15T17:30:08+09:00
tags : ["js"]
categories: "study"
comments: true
draft: false
---

## constructor

쉽게 설명하자면 `object`를 만들어주는 기계라고 생각하면 된다. 예를 들어서 우리가 각 학생에 대한 정보를 오브젝트로 저장한다고 하자.

```js
var 학생1 = { name : 'Kim', age : 15 };
var 학생2 = { name : 'Park', age : 15 };
...
```

이런 식으로 하드코딩하는 것보다 비슷한 오브젝트이니 복사해주는 것이 좋다. 하지만 오브젝트는 `reference type`이라서 단순히 등호(`=`)를 이용해서 복사하게 되면 문제가 발생한다.

그래서 우리는 이러한 오브젝트들을 찍어내는 기계를 이용하는데 이것이 바로 `constructor`이다.

```js
function 기계(){
  this.name = 'Kim';
  this.age = 15;
}
```

이런 식으로 사용하게 되는데 여기서 `this`의 의미는 새로 생성되는 오브젝트를 뜻하고 이것을 `인스턴스`라고 부른다. 위의 `기계`는 `{ name = 'Kim', age = 15 }`라는 오브젝트를 생성하게 되는데 생성할 때는 다음과 같이 사용해주면 된다.

```js
function 기계(){
  this.name = 'Kim';
  this.age = 15;
}

var 학생1 = new 기계();
var 학생2 = new 기계();
```

여기서 오브젝트에 함수도 추가해줄 수 있다. `sayhi`라는 함수를 통해서 이름이 들어간 인사를 출력해주는 함수를 넣고 싶다면 다음과 같이 해주면 된다.

```js
function 기계(){
  this.name = 'Kim';
  this.age = 15;
  this.sayHi = function(){
    console.log('안녕하세요' + this.name + ' 입니다');
  }
}
var 학생1 = new 기계();
var 학생2 = new 기계();

학생2.sayHi();
```

이렇게 만들어진 오브젝트에는 한가지 단점이 있는데 모두 같은 이름과 나이를 가진 오브젝트가 생성된다는 것이다. 각각의 속성들을 다르게 해주고 싶다면 `파라미터`를 이용하면 된다.

```js
function 기계(이름){
  this.name = 이름;
  this.age = 15;
  this.sayHi = function(){
    console.log('안녕하세요' + this.name + ' 입니다');
  }
}
var 학생1 = new 기계('Park');
var 학생2 = new 기계('Kim');
```

이렇게 `constructor`가 가진 속성을 그대로 물려받은 `오브젝트`를 생성하는 것을 `상속(inheritance)`이라고 한다.

## prototype

근데 js에는 `constructor`말고도 상속 기능을 구현하는 방법이 있다. 바로 `prototype`이다. 우리가 만든 `constructor`들은 `prototype`을 자동으로 생성한다. 다음과 같은 방법으로 확인할 수 있다.

```js
function 기계(){
  this.name = 'Kim';
  this.age = 15;
}

console.log(기계.prototype);
```

여기서 `prototype`는 비유하자면 일종의 부모의 유전자 역활을 한다고 보면 된다. 때문에 `기계.prototype`에 무언가 변수나 함수가 들어있다면 `기계`로부터 만들어진 자식들도 물려받아서 사용이 가능하다.

```js
function 기계(){
  this.name = 'Kim';
  this.age = 15;
}

기계.prototype.gender = '남';
var 학생1 = new 기계();

console.log(학생1.gender); //'남'이 출력된다.
```

이렇게 `prototype`을 이용해서 `gender`를 추가해주면 `기계`로 만든 모든 오브젝트에서 `gender`라는 속성을 사용할 수 있다. 이런 값들을 여러개 부여할 수도 있고 심지어 함수도 집어넣을 수 있다.

하지만 이렇게 추가된 데이터는 자식이 직접 가지고 있는 것이 아니고 부모만 가지고 있다.

### 작동 원리

```js
function 기계(){
  this.name = 'Kim';
  this.age = 15;
}

기계.prototype.gender = '남';
var 학생1 = new 기계();

console.log(학생1.gender); //'남'이 출력된다.
```

해당 코드에서 오브젝트에서 값을 출력할 때 다음과 같은 순서로 물어본다.

1. 학생1에 `gender`라는 값이 있는가?
2. 그럼 부모 `prototype`에 값이 있는가?
3. 그럼 부모의 부모 `prototype`에 있는가?
4. 그럼 부모의 부모의 ... `prototype`에 있는가?

따라서 학생1이라는 오브젝트에는 `gender`라는 값은 없지만 부모의 `prototype`에는 존재하기 때문에 출력할 수 있는 것이다.

### 내장 함수

우리가 `array`의 `toString()` 같은 내장함수를 사용할 수 있는 것도 같은 원리이다.

```js
var arr = [1,2,3];
console.log( arr.toString() ); //가능
```

이런 식으로 `arr.toString()` 이렇게 붙일 수 있는 이유는 `array`의 부모 `prototype`이 `toString()`이라는 함수를 가지고 있기 때문이다.

우리가 array나 object 자료형을 만들 때는 실제로 이런 식으로 만들어진다.

```js
var arr = [1,2,3];
var arr = new Array(1,2,3);
```

우리는 위의 방식으로 만들지만 사실은 아래와 같은 방식으로 만들어진다. 때문에 `arr`의 타입을 출력해보면 오브젝트로 나온다.

```js
console.log(typeof arr); //object
```

진짜로 `toString()`이라는 함수가 `Array`의 `prototype`에 있는지는 직접 출력해보면 확인할 수 있다.

```js
console.log(Array.prototype);
```

![프로토타입](/img/js_prototype/Array_Prototype.png)

또한 MDN에 적혀진 문구도 이해할 수 있다.

![MDN](/img/js_prototype/toString_mdn.png)

`Object`라는 `Constructor`의 유전자(`prototype`)에 있는 `toString()` 함수라는 뜻이다.

### 특징

1. `prototype`은 `constructor` 함수에만 몰래 생성된다.

일반 `object`, `array` 이런거 만들어도 거기엔 `prototype`이 존재하지 않는다. 만약 일반 `object`를 상속하고 싶다면 `constructor`를 사용하거나 `Object.create()`를 사용하거나 `class`를 사용하는 셋중 하나를 사용하면 된다.

2. 내 부모의 `prototype`을 찾고 싶으면 `__proto__`를 출력해보면 된다.

부모로부터 생성된 자식 `object`들은 `__proto__`라는 속성이 있다. 이것은 부모의 `prototype`을 나타낸다.

```js
function 기계(){
  this.name = 'Kim';
  this.age = 15;
}
var 학생1 = new 기계();
console.log(학생1.__proto__);
console.log(기계.prototype);
```

따라서 이렇게 출력해보면 둘이 같은 것을 알 수 있다.

3. `__proto__`를 직접 등록하면 object끼리 상속기능을 구현할 수 있다.

`__proto__`는 부모의 `prototype`을 의미한다고 했는데 이를 직접 설정해주면 어떻게 될까? 그럼 직접 설정해준 것이 부모가 된다.

```js
var 부모 = { name : 'Kim' };
var 자식 = {};

자식.__proto__ = 부모;
console.log(자식.name);
```

이렇게 되면 자식의 `prototype`은 `{ name : 'Kim' }`이라는 오브젝트가 된다.

4. 실은 `console`에서 `prototype` 정보들은 항상 출력된다.

```js
function 기계(){
  this.name = 'Kim';
  this.age = 15;
}

var 학생1 = new 기계();

console.log(학생1)
```

![console_prototype](/img/js_prototype/console.png)

여기서 더 나가아서 부모의 `prototype`도 확인할 수 있다. 이렇게 확인하면 결국 `Object()`라는 `constructor`가 나오게 된다. 그래서 자바스크립트는 모든게 다 `Object`라고 말하는 것이다!

## constructor vs prototype

그래서 어느 상황에서 `constructor`를 사용하고 어느 상황에서 `prototype`를 사용하면 되는 걸까?

자식들이 값을 직접 소유하게 하고 싶으면 `constructor`를 사용해서 상속시키면 되고 부모만 가지고 참조해서 쓰고 싶으면 `prototype`를 사용하면 된다. 그래서 보통 함수같은 것들을 `prototype`로 많이 사용한다.
