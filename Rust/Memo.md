# Rust

## 参考記事
- [なぜRustなの？と言われた時のために](https://zenn.dev/khale/articles/rust-beginners-catchup#rust-%E3%81%AF%E3%82%A8%E3%83%A9%E3%83%BC%E5%87%A6%E7%90%86%E3%81%8C%E5%88%86%E3%81%8B%E3%82%8A%E3%82%84%E3%81%99%E3%81%84)
- [Rust入門](https://zenn.dev/mebiusbox/books/22d4c1ed9b0003)
- [公式ドキュメント](https://doc.rust-lang.org/book/)

## Rustの概要
1. メモリ安全な言語

    メモリ管理には、従来、
    - プログラマが管理する: C言語
    - システムがGCによって自動で不要なメモリをかき集める: Java, Python
    の二種類があったが、Rustではこれ以外の手法を採用している。
    所有権という考え方のもと、以下のルールがある。
    ① 値は、変数が束縛しており、変数のことを所有者と呼ぶ
    ② 値の所有者は、その瞬間は1つの変数のみ
    ③ 所有者である変数のスコープを抜けた際に、その値は利用不可になる
    ④ 借用と言う考え方により、所有権を貸し出すことができる
    以下に、例を示す。

    1. 関数外スコープにおける変数へのアクセス

        ```Rust:
        fn f() {
            let s = "hello".to_string();
            // sを使った処理
        }
        // ここではsにアクセスすることはできない
        ```

    2. 関数に値を直接渡した際の所有権剥奪

        ___
        get_lengthにsを渡すと、sの所有者はget_length内のsに移る。
        ルール②より、get_lengt以降f()ではsにアクセスすることができない。
        ___
        ```Rust:
        fn get_length(s: &String) -> usize {
            s.len()
        }

        fn f() {
            let s = "hello".to_string();
            let len = get_length(s);
            // ここではsにアクセスすことができない
        }
        ```

    3. 別の引数に値を代入した際の所有権剥奪

        ___
        別の変数に代入した場合も、ルール②により"hello"の所有権が移る。
        これをRustではmoveと呼ぶ。
        ___
        ```Rust:
        fn f() {
            let s = "hello".to_string();
            let t = s;
            // ここではsにアクセスすることはできない
        }
        ```

    4. 所有権の借用

        ___
        ルール④の借用により、所有権をread-onlyでレンタルすることができる。
        借用は、sがimmutableの場合のみ可能である。（Rustではデフォルトで変数はfinal）
        ここで、immutableとはフィールドの値を変更できないクラス。
        ___
        ```Rust:
        fn get_lengt(s: &String) {
            s.len()
        }

        fn f() {
            let s = "hello".to_string();
            let t = &s;
            // sにアクセスすることが可能
            let len = get_length(&s);
            // sにアクセスすることが可能
        }
        ```

    このような所有権の仕組みは、以下のような優位点がある。

    - 実行する前に、コンパイル時点でエラーを出力するため、メモリ開放忘れによる実行中メモリリークが起きづらい
    - プログラマが手出しできないGCがないため、すべてのメモリリークの要員はコード上に存在する

1. リッチな型システム
  - struct

    ___
    直積型。C言語でのstruct。
    ___

    ```Rust:
    #[derive(Debug)]
    struct Person {
        name: String,
        age: u8,
    }

    fn f() {
        let taro = {
            name: String::from("taro"),
            age: 27,
        };
        println!("{:?}, taro")
    }
    ```

  - enum

    ___
    列挙型（複数の定数を一つのクラスとしてまとめておくことができる型）。
    JavaのEnumと同じ考え方だが、列挙定数以外も持てる。
    ___
    ```Rust:
    enum IpAddrKind {
        v4,
        v6,
    }

    fn f() {
        let v4 = IpAddrKind::v4;
        let v6 = IpAddrKind::v6;

        println!("{:?} {:?}", v4, v6);
    }
    ```

  - 直和型
    ___
    取りうるすべての型の網羅。TypeScriptではa = number | stringのように表現される。
    直和型とは、いくつかの方のうち一つだけを保持するような型。
    ___
    ```Rust:
    pub enum Action {
        Add {
            text: String,
        },
        Done {
            posistion: usize,
        },
        List,
    }
    ```

    - trait

    ___
    共通の振る舞いを定義する。structに付与することで、クラスのような振る舞いが可能。
    ___

    ```trait:
    struct person {
        name: String,
        age: u8,
    }

    pub trait Judge {
        fn isOver30(&self) -> bool;
    }

    impl Judge for person {
        fn isOver30(&self) -> bool {
            self.age > 30
        }
    }
    ```

    型システムが豊富なことにより、以下の優位点がある。
    - ドメイン知識を実装する幅が広がる

        Javaでは列挙型に対して、以下の制約がある。
        - 変数が持てない
        - 列挙ごとに変数の数は固定

        ```Java:
        enum IpAddr {
            v4("127.0.0.1"),
            v6("::1"),

            private final String loopBack;

            public String getLoopBack() {
                return this.loopBack;
            }
        }
        ```

        Rustでは、以下のように列挙値をそれぞれ別の型で表現することができる。（直和型）
        ```Rust:
        enum IpAddr {
            v4 (u8, u8, u8, u8),    // 8Byte整数値を4つ持つタプル
            v6 {loopBack: String},  // Stringを1つ持つstruct
        }

        fn f() {
            let v4LoopBack = IpAddr::V4(127, 0, 0, 1);
            let v6LoopBack = IpAddr::V6 {
                ip: "::1".to_string(),
            };
            println!("{:?}, {:?}", v4LoopBack, v6LoopBack); // V4(127, 0, 0, 1), V6 { ip: "::1" }
        }
        ```

    - パターンマッチングによる分岐処理が簡潔にかける

        ___
        actionの型を判定し、後続の処理につなげる。
        ___
        ```Rust:
        pub enum Action {
            Add {text: String, },
            Done {position: usize, },
            List,
        }

        match action {
            Add { text } => ...,        // 文字列の場合の処理
            List => ...,                // 何も指定されなかった場合の処理
            Done { posision } => ...,   // 数値の場合の処理
        }
        ```

- エラー処理がわかりやすい

    - 検査例外

        以下の２つの列挙型を返り値とすることで実現される。
        ```Rust:
        pub enum Result<T, E> {
            OK(T),
            Err(E),
        }

        pub enum Option<T> {
            None,
            Some(T),
        }
        ```
        Result

    - 非検査例外

        panic!を発生することで実現される。
        panic!が発生すると、デフォルトではこれまで確保したメモリ等を自動的に開放していく。
        ```Rust:
        fn main() {
            panic!("crash and burn");
        }
        ```


