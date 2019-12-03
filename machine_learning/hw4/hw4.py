#!/usr/bin/env python
# coding: utf-8

import gym
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from torch.distributions import Categorical

env = gym.make('CartPole-v1')
eps = np.finfo(np.float32).eps.item()
gamma = 0.99


class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()
        self.fc1 = nn.Sequential(
            nn.Linear(4, 24),
            nn.ReLU(),
        )
        self.fc2 = nn.Sequential(
            nn.Linear(24, 36),
            nn.Dropout(p=0.7),
            nn.ReLU(),
        )
        self.fc3 = nn.Linear(36, 2)

        self.saved_log_probs = []
        self.rewards = []
        self.sumrewards = []

    def forward(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        return F.softmax(x, dim=1)


policy = Policy()
optimizer = optim.Adam(policy.parameters(), lr=1e-2)


def select_action(state):
    state = torch.from_numpy(state).float().unsqueeze(0)
    probs = policy(state)  # FORWARD PASS
    m = Categorical(probs)
    action = m.sample()
    policy.saved_log_probs.append(m.log_prob(action))
    return action.item()


def finish_episode_and_update():
    R = 0
    policy_loss = []
    returns = []
    for r in policy.rewards[::-1]:
        R = r + gamma * R
        returns.insert(0, R)
    print("R", R)
    policy.sumrewards.append(R)
    returns = torch.tensor(returns)
    returns = (returns - returns.mean()) / (returns.std() + eps)
    for log_prob, R in zip(policy.saved_log_probs, returns):
        policy_loss.append(-log_prob * R)
    optimizer.zero_grad()
    policy_loss = torch.cat(policy_loss).sum()
    policy_loss.backward()  # backward pass
    optimizer.step()
    del policy.rewards[:]
    del policy.saved_log_probs[:]


def main():
    num_episodes = 1000
    for _ in range(num_episodes):
        state = env.reset()  # reset() resets the environment
        episode_reward = 0
        for t in range(1, 10000):  # no of steps
            action = select_action(state)
            state, reward, done, _ = env.step(action)
            env.render()  # show
            policy.rewards.append(reward)
            episode_reward += reward
            if done:
                print("episode ended!")
                break
        finish_episode_and_update()


main()
plt.figure(num=1)
plt.plot(policy.sumrewards, label="rewards")
plt.legend()
plt.xlabel("Number of epochs")
plt.ylabel("The reward")
plt.title("The reward of hw5-a")
plt.savefig("hw5_a.jpg")
plt.close()



