def preprocess_board(board):
    """
    Normalize the game board for neural network input.
    Convert tiles to log2 values and scale to [0, 1].
    """
    return np.log2(np.array(board, dtype=np.float32) + 1) / 16  # Normalize by 16 (max tile exponent for 65536)

import torch
import torch.nn as nn
import torch.optim as optim

directions = {0:[0,-1],1:[0,1],2:[1,0],3:[-1,0]}
location = {
    (0, 0):0,
    (0, 1):0,
    (0, 2):1,
    (0, 3):1,
    (1, 0):0,
    (1, 1):0,
    (1, 2):1,
    (1, 3):1,
    (2, 0):2,
    (2, 1):2,
    (2, 2):3,
    (2, 3):3,
    (3, 0):2,
    (3, 1):2,
    (3, 2):3,
    (3, 3):3
}

class PPOModel(nn.Module):
    def __init__(self):
        super(PPOModel, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 128, kernel_size=2, stride=1),
            nn.ReLU(),
            nn.Flatten()
        )
        self.policy = nn.Sequential(
            nn.Linear(128 * 9, 256),
            nn.ReLU(),
            nn.Linear(256, 4),  # 4 actions (up, down, left, right)
            nn.Softmax(dim=-1)
        )
        self.value = nn.Sequential(
            nn.Linear(128 * 9, 256),
            nn.ReLU(),
            nn.Linear(256, 1)
        )

    def forward(self, x):
        x = self.conv(x)
        return self.policy(x), self.value(x)
