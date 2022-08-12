---
title: "백준 2457번 공주님의 정원"
description: "공주님의 정원 풀이 및 풀면서 느낌점"
date: 2022-08-13
update: 2022-08-13
tags:
  - Algorithm
  - Greedy
---

# 2457번 공주님의 정원

[백준 링크](https://www.acmicpc.net/problem/2457)

## 문제 요약

그리디 알고리즘을 사용해서 꽃의 최소의 갯수를 구하는 문제이다.

## 과정

처음에는 꽃이 지는 시간을 기준으로 내림차순, 꽃이 피는 시간을 기준으로  오름차순으로 정렬해서 풀었다.
앞에서부터 탐색해서 끝나는 시간이 제일 긴 것을 골라서 갱신하는 방식이였다.

하지만 계속 앞에서부터 탐색하면서 불필요한 탐색이 많아졌고, 최대 입력이 10만개라서 85% 쯤에서 시간 초과가 일어났다.

그래서 다른 방식으로 풀기로 했다.

## 풀이 과정

정렬을 꽃이 피는 시간을 기준으로 오름차순으로 정렬하고, 지는 시간을 기준으로 내림차순으로 정렬한다.

꽃의 시간은 숫자의 형태로 저장한다.
`flowers.start = 301`
왜냐하면 만약 월수가 같더라도 비교하기 쉽고 저장하기 쉽기 때문에 이렇게 저장해서 사용했다.

비교를 시작하는데 11월 30일까지 펴야하는데 지는 꽃의 숫자는 포함하지 않기 때문에 12월 1일을 넘길때까지 비교를 반복하게 되었다.

비교하는 중에 비교하는 꽃의 끝이 배열에 담긴 꽃의 시작보다 작다면 비교하는 의미가 없기 때문에 비교를 그만둔다.

그 후에 지는 시간을 비교하면서 가장 큰 값을 찾고 값을 찾았음을 기록해주었다.

그 후에 만약 값을 찾지 못했다면 다음 꽃이 없다는 것을 의미함으로 바로 끝내주었고 아니라면 비교할 값을 갱신하고 꽃의 갯수를 늘려주었다.

## 코드
```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.StringTokenizer;

public class algo_2457 {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int flowerCnt = Integer.parseInt(br.readLine().trim());
        Flower[] flowers = new Flower[flowerCnt];
        StringTokenizer st;
        for (int i = 0; i < flowerCnt; i++) {
            st = new StringTokenizer(br.readLine().trim(), " ");
            int startMonth = Integer.parseInt(st.nextToken());
            int startDay = Integer.parseInt(st.nextToken());
            int endMonth = Integer.parseInt(st.nextToken());
            int endDay = Integer.parseInt(st.nextToken());
            flowers[i] = new Flower(startMonth * 100 + startDay, endMonth * 100 + endDay);
        }

        Arrays.sort(flowers);

        int startDay = 301;
        int endDay = 1201;
        int count = 0;
        int max = 0;
        int startIdx = 0;
        boolean isFind = false;

        while (startDay < endDay) {
            isFind = false;
            for (int i = startIdx; i < flowerCnt; i++) {
                if (flowers[i].start > startDay) {
                    break;
                }
                if (max < flowers[i].end) {
                    max = flowers[i].end;
                    startIdx = i + 1;
                    isFind = true;
                }
            }
            if (isFind) {
                startDay = max;
                count += 1;
            } else {
                break;
            }
        }
        if (max < endDay) {
            System.out.println(0);
        } else {
            System.out.println(count);
        }

    }

    static class Flower implements Comparable<Flower> {
        int start;
        int end;

        public Flower(int start, int end) {
            this.start = start;
            this.end = end;
        }

        @Override
        public int compareTo(Flower f) {
            if (this.start != f.start) {
                return this.start - f.start;
            } else {
                return -this.end + f.end;
            }
        }
    }
}
```

## 풀면서 배운 것

1. 시간(월, 일)을 비교할 때는 숫자형식으로 비교하는 것이 더 편하다.
2. 어떤 객체를 비교하는 경우 클래스로 따로 빼서 만들어서 비교하면 코드 가독성이 더 좋아진다.
