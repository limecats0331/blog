---
title : watering
description : baekjoon 1368 물대기
date : 2022-09-01
update : 2022-09-01
tags :
  - Baekjoon
  - MST
series : Algorithm
---

[문제 링크](https://www.acmicpc.net/problem/1368)

## 문제 요약

N개의 논에 물을 대야 하는데 방법이 2가지 있다.
하나는 직접 논에 우물을 파는 것이고 다른 하나는 이미 물이 있는 논에서 물을 끌어오는 방법이다.
각 논에서 우물을 파는 비용과 다른 논 사이에서 물을 끌어오는 비용이 주어질 때 모든 논에 물을 대는 최소값을 구하여라.

## 문제 풀이

처음에는 논 중에 최소비용으로 팔 수 있는 곳을 찾아서 거기서부터 최소 신장 트리를 구해서 값을 구하고자 했다.

하지만 제대로 구해지지 않았고 이후 검색을 통해 최소 신장 트리는 노드가 아닌 엣지를 기준으로 검색하는 것이니깐 자기 자신이 우물을 파는 것을 임의의 노드에서 출발하는 값이라고 생각하고 풀면 쉽게 풀 수 있다는 것을 알게 되었다.

굳이 풀어서 설명하자면 우물을 통해서 지하에서 물을 끌어오는 것이라고 생각하고 지하도 노드에 추가하는 것이다.

그래서 입력받을 때 우물을 파는 것은 0에서 연결한다고 생각하고 엣지를 만들어서 크루스칼을 이용해서 풀었다.

## 코드

```java
import java.io.*;
import java.util.*;

public class algo_1368 {
    static int[] root;

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int N = Integer.parseInt(br.readLine().trim());

        makeSet(N + 1);

        List<Node> nodes = new ArrayList<>();

        for (int i = 0; i < N; i++) {
            nodes.add(new Node(0, i + 1, Integer.parseInt(br.readLine().trim())));
        }

        for (int i = 0; i < N; i++) {
            String[] input = br.readLine().trim().split(" ");
            for (int j = 0; j < N; j++) {
                if (i == j) continue;
                nodes.add(new Node(i + 1, j + 1, Integer.parseInt(input[j])));
            }
        }

        Collections.sort(nodes);

        int res = 0;
        int cnt = 0;
        for (Node n : nodes) {
            if (unionSet(n.from, n.to)) {
                res += n.weight;
                cnt += 1;
            }
            if (cnt == N) {
                break;
            }
        }

        System.out.println(res);
    }

    static boolean unionSet(int from, int to) {
        from = findRoot(from);
        to = findRoot(to);
        if (from == to) return false;
        root[from] = to;
        return true;    }

    static int findRoot(int n) {
        if (n == root[n]) return n;
        return root[n] = findRoot(root[n]);
    }

    static void makeSet(int N) {
        root = new int[N];
        for (int i = 0; i < N; i++) {
            root[i] = i;
        }
    }

    static class Node implements Comparable<Node> {
        int from;
        int to;
        int weight;

        public Node(int from, int to, int weight) {
            this.from = from;
            this.to = to;
            this.weight = weight;
        }

        @Override
        public int compareTo(Node n) {
            return this.weight - n.weight;
        }
    }
}
```


## 배운 점

최소 신장 트리는 엣지를 기준으로 생각하자 엣지가 없다면 임의의 노드에서 연결하는 엣지를 만들어서 생각해볼 수 있다.
