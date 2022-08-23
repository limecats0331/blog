---
title: "백준 1912번 연속합"
description: "백준 연속합 정리"
date: 2022-08-13
update: 2022-08-13
tags:
  - Baekjoon
  - DP
series : "Algorithm"
---

[문제링크](https://www.acmicpc.net/problem/1912)

## 문제 요약

크기가 10만개 이하인 정수로 이루어진 수열이 주어질 때, 연속된 숫자들의 합 중에 가장 큰 수를 구하는 문제

## 풀이 과정

풀면서 중요했던 점은 이전까지의 과정에서 구한 최대 연속합을 더했을 때 손해(더  작아짐)라면 버리고 새로 더하는 것이다.

### 예시

| index   | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arrs | 10  | -4  | 3   | 1   | 5   | 6   | -35 | 12  | 21  | -1  |

수열이 다음과 같이 주어진다고 생각해본다.
여기서 특정 구간까지의 연속합을 `dp`라고 생각한다.

| index | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arrs  | 10  | -4  | 3   | 1   | 5   | 6   | -35 | 12  | 21  | -1  |
| dp    | 10  | 6   | 9   | 10  | 15  | 21  | -14 | 12  | 33  | 32  |

그럼 0까지의 연속합은 10이 되고 1까지의 연속합의 최대는 6이 된다.

이렇게 6까진 마치 누적합과 같은 모습을 보이게 된다.

하지만 6에서 7로 넘어갈 때를 보면 7의 입장에서 보면 이전까지의 연속합을 더 하는 것이 자신보다 더 작아지게 됨으로 가장 큰 연속합은 아무것도 더하지 않은 자기 자신이 된다.

따라서 7부터 다시 연속된 합을 찾아가는  것이다.

이것을 코드로 표현한다면 다음과 같이 표현할 수 있다.

```java
dp[i] = Math.max(dp[i-1] + arrs[i], arrs[i]);
```

## 코드

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class algo_1912 {
    public static void main(String[] args) throws Exception {
	    //입력
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int[] dp = new int[n];

		//숫자를 따로 저장할 필요없이 입력받은 대로 찾을 수 있음.
        StringTokenizer st = new StringTokenizer(br.readLine().trim(), " ");
        dp[0] = Integer.parseInt(st.nextToken());
        //dp[0]는 첫번째 숫자와 같다.
        int max = dp[0];
        //숫자의 갯수만큼 반복해준다.
        for (int i = 1; i < n; i++) {
            int num = Integer.parseInt(st.nextToken());
            dp[i] = Math.max(dp[i - 1] + num, num);
            max = Math.max(max, dp[i]);
        }
        System.out.println(max);
    }
}
```

## 배운 점

앞까지 구한 것이 손해라면 새로 시작한다는 개념 생각할 수 있게 되어서 좋았다.
