import tkinter as tk, random
from math import sin, cos, hypot
# 要素を非表示にする関数
def back_title():
    scale2.pack_forget()
    canvas.pack_forget()
    button1.pack_forget()
    button2.pack_forget()
    frame2.pack_forget()
    text1.pack_forget()
    text2.pack_forget()
    button3.pack_forget()
    root.after(1,pack_title1)
def start_game():
    title.pack_forget()
    frame1.pack_forget()
    button_vsp.pack_forget()
    button_vsc.pack_forget()
    scale1.pack_forget()
    root.after(1,pack_game1)
# vsプレイヤーとvsコンピューターの関数
def vsp():
    global vs
    vs = 0
    start_game()
def vsc():
    global vs
    vs = random.choice([-1, 1])
    start_game()
# なんか上手くいかなかったので、2つに分けてみたら上手くいった、要素を表示する関数
def pack_title1():
    title.pack(side="top", fill="both", expand=True, padx=10)
    frame1.pack(side="top", fill="both", expand=True)
    root.after(1,pack_title2)
def pack_title2():
    button_vsp.pack(side="left", fill="both", expand=True, padx=10)
    button_vsc.pack(side="left", fill="both", expand=True, padx=10)
    scale1.pack(side="bottom", fill="both", expand=True, padx=10)
def pack_game1():
    scale2.pack(side="top", fill="both", expand=True, padx=10)
    canvas.pack(side="top")
    button1.pack(side="top", fill="both", expand=True, padx=10)
    button2.pack(side="left", fill="both", expand=True, padx=10)
    frame2.pack(side="left", fill="both", expand=True)
    root.after(1,pack_game2)
def pack_game2():
    text1.pack(side="top", fill="both", expand=True)
    text2.pack(side="bottom", fill="both", expand=True)
    button3.pack(side="left", fill="both", expand=True, padx=10)
    game_reset()
# クリックされた関数
def click(event):
    global touch_point1
    touch_point1 = []
    # クリック時のマス
    for point in points:
        if hypot(event.x-point[0], event.y-point[1]) <= R:
            touch_point1 = point
    # マスをクリック出来ていないなら
    if len(touch_point1) == 0 or board[touch_point1[5]][touch_point1[4]][touch_point1[3]] or vs == -turn:
        touch_point1 = []
# クリックが離された関数
def release(event):
    global turn
    # マスをクリック出来ていたか
    if len(touch_point1) > 0:
        touch_point2 = []
        # 離す時のマス
        for point in points:
            if hypot(event.x-point[0], event.y-point[1]) <= R:
                touch_point2 = point
        # マスを押したのなら
        if len(touch_point2) > 0 and touch_point1 == touch_point2:
            getsquares = []
            # 全方向に判定
            for dir in directions:
                getsquares += dirgets(dir, touch_point1[3], touch_point1[4], touch_point1[5])
            # 取れるなら
            if len(getsquares):
                # 取る
                board[touch_point2[5]][touch_point2[4]][touch_point2[3]] = turn
                for get in getsquares:
                    board[get[2]][get[1]][get[0]] = turn
                draw()
                # スコア更新
                score_update(len(getsquares))
                # 相手の番に
                pas()
# 描画する関数
def draw():
    global points, R
    R = scale2.get()*LENGTH/(300*NUM)
    canvas.delete("all")
    points = []
    # 座標計算
    for k in range(NUM):
        for j in range(NUM):
            for i in range(NUM):
                # 回転計算
                rolled_x, rolled_y, rolled_z = (i-NUM/2+0.5)*cos(alpha) - (k-NUM/2+0.5)*sin(alpha), j - NUM/2 + 0.5, (i-NUM/2+0.5)*sin(alpha) + (k-NUM/2+0.5)*cos(alpha)
                rolled_y, rolled_z = rolled_y*cos(beta) + rolled_z*sin(beta), rolled_y*sin(beta) - rolled_z*cos(beta)
                # 中心合わせ
                points.append((LENGTH*rolled_x/(3*NUM/2) + LENGTH/2, LENGTH*rolled_y/(3*NUM/2) + LENGTH/2, LENGTH*rolled_z/(3*NUM/2) + LENGTH/2, i+1, j+1, k+1))
    # 奥行き順に
    points = sorted(points, key=lambda z: z[2])
    # 奥ほど暗くマスを描画
    for x_pos, y_pos, z_pos, i, j, k in points:
        brightness = 0.5 + z_pos/1400
        canvas.create_oval(x_pos-R, y_pos-R, x_pos+R, y_pos+R, fill=adjust_brightness(color[board[k][j][i]], brightness), outline="yellow", width=int(0.15*R))
# 1方向判定関数
def dirgets(dir, x0, y0, z0):
    dir_getsquares = []
    # 置いた場所
    current_x, current_y, current_z = x0, y0, z0
    # 確認していく
    while True:
        current_x += dir[0]
        current_y += dir[1]
        current_z += dir[2]
        if not board[current_z][current_y][current_x] == -turn:
            break
        dir_getsquares.append((current_x, current_y, current_z))
    # 取れない場合
    if not board[current_z][current_y][current_x] == turn:
        dir_getsquares = []
    return dir_getsquares
# 回転させる関数
def roll(event):
    global alpha, beta, ang_vel, delay_id
    # 押されたキー
    key = event.keysym
    # 矢印キーなら
    if key == "Right" or key  == "Left" or key == "Up"  or key == "Down":
        try:
            # 長押しでリセットタイマーリセット
            root.after_cancel(delay_id)
        except:
            # 初回
            pass
        # 回転させる
        if key == "Right":
            alpha += ang_vel
        elif key == "Left":
            alpha -= ang_vel
        elif key == "Up":
            beta += ang_vel
        else:
            beta -= ang_vel
        draw()
        # 角速度アップ
        ang_vel = min(max_ang_vel, ang_vel + ang_accel)
        # 0.2秒後角速度リセットタイマー
        delay_id = root.after(200, ang_vel_reset)
# 奥ほど暗くする関数
def adjust_brightness(hex_color, brightness):
    # 16進数でr、g、bに分ける
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    # 暗くする
    r = int(r * brightness)
    g = int(g * brightness)
    b = int(b * brightness)
    # 合体させる
    adjusted_color = f"#{r:02x}{g:02x}{b:02x}"
    return adjusted_color
# 角速度を初期化する関数
def ang_vel_reset():
    global ang_vel
    ang_vel = start_ang_vel
# 角度を初期化する関数
def reset_theta():
    global alpha, beta
    # 角度を初期化
    alpha, beta = -0.2, -0.3
    draw()
# 全てを初期化する関数
def game_reset():
    global board, turn, score
    # 外枠を2、空きマスを0としてNUM^3の盤面を作成
    board = [[[2 if i%(NUM+1) == 0 or j%(NUM+1) == 0 or k%(NUM+1) == 0 else 0 for i in range(NUM+2)] for j in range(NUM+2)] for k in range(NUM+2)]
    center = int(NUM/2)
    board[center][center][center:center+2], board[center][center+1][center:center+2] = [1, -1], [-1, 1]
    board[center+1][center][center:center+2], board[center+1][center+1][center:center+2] = [-1, 1], [1, -1]
    # スコア
    score = {1:4, -1:4}
    # 初手を黒に
    turn = 1
    # 表示
    text1["text"], text2["text"] = "黒の番", "4:4"
    reset_theta()
    ang_vel_reset()
    if vs == -1:
        text1["text"] += "(CPU)"
        root.after(cpu_delay, cpu)
    elif vs:
        text1["text"] += "(あなた)"
# パスボタンの関数
def pass_button():
    if not vs == -turn:
        pas()
# パスする関数
def pas():
    global turn
    # 相手のターンに
    turn = -turn
    text1["text"] = turn_color[turn] + "の番"
    if vs == -turn:
        text1["text"] += "(CPU)"
        root.after(cpu_delay, cpu)
    elif vs:
        text1["text"] += "(あなた)"
# cpuの関数
def cpu():
    getsquares = []
    # 置けるマスを確認
    for k in range(1, NUM+1):
        for j in range(1, NUM+1):
            for i in range(1, NUM+1):
                if board[k][j][i] == 0:
                    getsquare = []
                    # 全方向に判定
                    for dir in directions:
                        getsquare += dirgets(dir, i, j, k)
                    # 取れるなら
                    if len(getsquare) > 0:
                        getsquares.append((getsquare, i, j, k))
    # 置けるマスがあるなら
    if len(getsquares) > 0:
        getsquares, i, j, k = random.choice(getsquares)
        # 取る
        board[k][j][i] = turn
        for get in getsquares:
            board[get[2]][get[1]][get[0]] = turn
        draw()
        # スコア更新
        score_update(len(getsquares))
    # 相手の番に
    pas()
# スコア更新の関数
def score_update(gets):
    score[turn] += 1 + gets
    score[-turn] -= gets
    text2["text"] = f"{score[1]}:{score[-1]}"
    if score[1]+score[-1] == NUM**3:
        if score[1] == score[-1]:
            text2["text"] += "で引き分け"
        else:
            text2["text"] += f"で{turn_color[(score[1]>score[-1])-(score[1]<score[-1])]}の勝ち"
# スライダー用の関数
def piece_num_change(value):
    global NUM
    NUM = int(value)
def dr(_):
    draw()
# rootを作成
root = tk.Tk()
root.title("3Dオセロ")
# ウインドウのサイズをLENGTHに固定
LENGTH = int(root.winfo_screenheight()*0.85) - 160
root.geometry(f"{LENGTH}x{LENGTH+160}")
root.resizable(False, False)
# マスの数(1辺)
NUM = 4
# マスのサイズ
R = 0.7 * LENGTH / (300*NUM)
# 緑、黒、白
color = ["#00FF00", "#000000", "#FFFFFF"]
# 26方向のリストを作成
directions = [(i, j, k) for i in range(-1,2) for j in range(-1,2) for k in range(-1,2) if not i == j == k == 0]
# 1を黒に、-1を白に
turn_color = {1:"黒", -1:"白"}
# 初期角速度、最大角速度、角加速度
start_ang_vel, max_ang_vel, ang_accel = 0.01, 0.15, 0.004
ang_vel = start_ang_vel
# 敵の待ち時間
cpu_delay = 1000
# 角度を初期化
alpha, beta = -0.2, -0.3
# 要素を作成
title=tk.Label(root, text="3Dオセロ", font=("Arial", int(LENGTH/10)))
frame1 = tk.Frame(root)
button_vsp = tk.Button(frame1, text="vs プレイヤー", font=("Arial", int(LENGTH/20)), command=vsp)
button_vsc = tk.Button(frame1, text="vs コンピューター", font=("Arial", int(LENGTH/20)), command=vsc)
scale1 = tk.Scale(root, label="1辺のマス数[個]", font=("Arial", int(LENGTH/30)), orient=tk.HORIZONTAL, width=int(LENGTH/60), from_=3, to=8, tickinterval=1, command=piece_num_change)
scale1.set(4)
scale2 = tk.Scale(root, label="マスのサイズ[%]", font=("Arial", int(LENGTH/40)), orient=tk.HORIZONTAL, width=int(LENGTH/60), from_=0, to=100, tickinterval=50, command=dr)
scale2.set(70)
canvas = tk.Canvas(root, width=LENGTH, height=LENGTH, bg="light blue")
button1 = tk.Button(root, text="パス", font=("Arial", int(LENGTH/30)), command=pass_button)
button2 = tk.Button(root, text="角度をリセット", font=("Arial", int(LENGTH/30)), command=reset_theta)
frame2 = tk.Frame(root)
text1 = tk.Label(frame2, text="黒の番", font=("Arial", int(LENGTH/40)))
text2 = tk.Label(frame2, text="4:4", font=("Arial", int(LENGTH/40)))
button3 = tk.Button(root, text="終わる", font=("Arial", int(LENGTH/30)), command=back_title)
# クリックされたら、離されたら、キーが押されたら
canvas.bind("<Button-1>", click)
canvas.bind("<ButtonRelease-1>", release)
root.bind("<Key>", roll)
# タイトル表示
pack_title1()
root.mainloop()