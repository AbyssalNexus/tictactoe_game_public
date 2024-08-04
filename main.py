import pygame
import sys

class tictactoe:
    def __init__(self) -> None:
        # 画面サイズ
        self.width = 600
        self.height = 600

        # 色の定義
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)

    def init_board(self):
        # 盤面を初期化
        return [['' for _ in range(3)] for _ in range(3)]
    
    def draw_board(self):
        # 線を描画
        for i in range(1, 3):
            pygame.draw.line(self.screen, self.black, (i * self.width // 3, 0), (i * self.width // 3, self.height), 2)
            pygame.draw.line(self.screen, self.black, (0, i * self.height // 3), (self.width, i * self.height // 3), 2)
        
        # マークを描画
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 'X':
                    x = col * self.width // 3 + self.width // 6
                    y = row * self.height // 3 + self.height // 6
                    pygame.draw.line(self.screen, self.red, (x - 50, y - 50), (x + 50, y + 50), 4)
                    pygame.draw.line(self.screen, self.red, (x + 50, y - 50), (x - 50, y + 50), 4)
                elif self.board[row][col] == 'O':
                    x = col * self.width // 3 + self.width // 6
                    y = row * self.height // 3 + self.height // 6
                    pygame.draw.circle(self.screen, self.blue, (x, y), 50, 4)

    def check_winner(self):
        # 横、縦、斜めのチェック
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        return None
    
    def is_board_full(self):
        return all(all(cell != '' for cell in row) for row in self.board)
    
    def start_game(self):
        # pygameの初期化
        pygame.init()
        self.font = pygame.font.Font("data/ipaexm.ttf", 40)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("三目並べ")
        
        while True:
            self.reset_game()
            self.game_loop()

    def reset_game(self):
        # ゲームのリセット
        self.board = self.init_board()
        self.current_player = 'X'
        self.game_over = False

    def game_loop(self):
        # ゲームループ
        while True:
            # イベント処理
            for event in pygame.event.get():
                # ウィンドウを閉じるボタンが押されたとき
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over:
                        return  # ゲームループを抜ける
                    
                    mouseX, mouseY = pygame.mouse.get_pos()
                    # クリックされたマス目を特定
                    clicked_row = mouseY // (self.height // 3)
                    clicked_col = mouseX // (self.width // 3)
                    
                    if self.board[clicked_row][clicked_col] == '':
                        # マス目が空の場合、マークを描画
                        self.board[clicked_row][clicked_col] = self.current_player
                        winner = self.check_winner()
                        if winner:
                            # 勝者がいる場合、ゲーム終了
                            self.game_over = True
                        elif self.is_board_full():
                            # 引き分けの場合、ゲーム終了
                            self.game_over = True
                        else:
                            # 次のプレイヤーに交代
                            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
            self.screen.fill(self.white)
            self.draw_board()
            
            if self.game_over:
                # ゲーム終了時のメッセージを描画
                if winner:
                    # 勝者がいる場合、勝者を表示
                    text = self.font.render(f"プレイヤー {winner} の勝利!", True, self.black)
                else:
                    # 引き分けの場合、引き分けを表示
                    text = self.font.render("引き分け!", True, self.black)
                text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
                # テキストを描画
                self.screen.blit(text, text_rect)
                
                # リスタート案内を表示
                restart_text = self.font.render("クリックしてリスタート", True, self.black)
                restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
                # テキストを描画
                self.screen.blit(restart_text, restart_rect)
            
            pygame.display.flip()


if __name__ == '__main__':
    game = tictactoe()
    game.start_game()