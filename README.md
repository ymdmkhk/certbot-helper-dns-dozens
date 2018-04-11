# certbot-helper-dns-dozens

Let's Encrypt のSSL/TLS サーバ証明書をCertbotで取得する際、[「Dozens（ダズンズ）」](https://dozens.jp/i/OaU0TF)を利用したDNSによる認証を自動化するための Python スクリプトです。(内部でcurlを使用しています。)「Dozens（ダズンズ）」](https://dozens.jp/i/OaU0TF)は無料でも使えるDNSサービスです。

<!-- ## Description -->

## Requirement 前提条件
- curl コマンドが使えること
- 証明書を取得したいドメインもしくはその親ドメインのゾーンが[Dozens](https://dozens.jp/i/OaU0TF)で管理されていること
- certbot が使えること

## Usage 使い方
1. [dns_dozens.py](https://raw.githubusercontent.com/ymdmkhk/certbot-helper-dns-dozens/master/dns_dozens.py)をダウンロードし、chmod u+x で実行可能にする
1. DozensのIDを環境変数 `DOZENS_ID`、API KEYを`DOZENS_KEY`にセットした上で、certbot のオプション --manual-auth-hook と--manual-cleanup-hook に dns_dozens.py を指定し、certbot を実行する
```bash
DOZENS_ID=your_id DOZENS_KEY=your_key certbot certonly --manual --preferred-challenges=dns --manual-auth-hook /path/to/script/dns_dozens.py --manual-cleanup-hook /path/to/script/dns_dozens.py -d secure.example.com
```
<!-- ## Contribution -->
## Limitations 制限事項
- Dozensに登録するドメイン(サブドメイン含む)に`"_"`が含まれている場合にうまく動かず、`"_acme-challenge.secure.example.com"` 自体をDozensのドメインに登録して使うことができない。(ドメインに`"_"`が使えないのはDozensのAPI自体の制限に見え、回避策がわからない。)
## Licence ライセンス

[Apache License 2.0](https://github.com/ymdmkhk/certbot-helper-dns-dozens/blob/master/LICENSE)

## Author 作者

[YAMADA Mikihiko](https://github.com/ymdmkhk)
