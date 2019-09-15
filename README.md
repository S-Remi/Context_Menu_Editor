# Context_Menu_Editor
コンテキストメニュー（右クリックメニュー）を追加するGUIアプリケーション。


cmdからregコマンドを使用しているため、Windows限定となります。

# 警告 warning
レジストリの編集を行います。このソフトの使用は自己責任で行ってください。


Edit the registry. Use this software at your own risk.

## コンテキストメニューの追加
add 部分の
「Text」にコンテキストメニューで表示される名前、
「command」にコンテキストメニューを実行したときのコマンドを入力し、

「Type」は以下の4種類から選択する。
 - "file"   : ファイルを選択した場合にコンテキストメニューを表示する。
 - "folder" : フォルダを選択した場合にコンテキストメニューを表示する。
 - "back"   : ファイル、フォルダのない場所を選択した場合にコンテキストメニューを表示する。
 - ".py"    : .pyファイルを選択した場合にコンテキストメニューを表示する。

Pythonを読める人なら、option_listに拡張子を、option_dictに{拡張子:"SystemFileAssociations\\拡張子"}
を追加するとType項目が増える。

例：

 option_list.append(".txt")
 option_dict[".txt"] = "SystemFileAssociations\\.txt"

項目を消す場合には必ず、消すType項目のコンテキストメニューを全て削除することを推奨する。
削除方法は下記参照。

「Type」、「Text」、「command」の全ての項目を埋めたら、
追加ボタンをクリックすると追加することができる。

## コンテキストメニューの削除

リスト表示されている部分の削除したい項目をクリックし、
delete 部分に削除したい項目が表示されたのを確認し、
削除ボタンをクリックすると削除することができる。

## あとがき
「コマンドウィンドウをここで開く」とか「このPythonを実行する」が欲しくて即席で作ったものの、
焦るあまりwinregに気付かずにコマンドプロンプトを呼び出してregコマンドを実行した奴←
そのため、実行がとっても遅い。（まぁ、当たり前

また、shellexのレジストリキーで実装されているコンテキストメニューをまだ理解していなかったため、
追加と追加したものの削除のみの実装となっている。
この事もあり、C++なんかで1から作り直そうかなとも考えている。

