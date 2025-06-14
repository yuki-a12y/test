# EC2 起動/停止 Lambda

このリポジトリには、入力イベントに応じて EC2 インスタンスを起動または停止するシンプルな AWS Lambda 関数が含まれています。

## ファイル構成

- `lambda/lambda_function.py` - `boto3` を利用した Lambda ハンドラー実装

## 使い方

1. `lambda` ディレクトリを ZIP 化するなどして Lambda 関数としてデプロイします（SAM など任意の方法で構いません）。
2. 環境変数 `INSTANCE_IDS` に対象とする EC2 インスタンス ID をコンマ区切りで指定します。
3. 関数実行時には以下のようなイベントを渡します。

```json
{ "action": "start" }
```

`action` には `start` または `stop` を指定できます。イベント側でインスタンス ID を上書きすることも可能です。

```json
{ "action": "stop", "instance_ids": ["i-12345678"] }
```

定期実行したい場合は CloudWatch Events や API Gateway などをトリガーとして利用してください。
