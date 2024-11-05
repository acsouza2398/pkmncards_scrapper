import torch.nn as nn
import torch

class AutoEncoder(nn.Module):
    """
    AutoEncoder class.

    """    
    def __init__(self, input_dim, hidden_dim):
        super(AutoEncoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32)
        )
        self.decoder = nn.Sequential(
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, input_dim)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
    
    def encode(self, x):
        """
        Encode the input data to the latent space.
        
        Args:
            x: Input tensor to encode.
        
        Returns:
            Encoded representation of the input.
        """
        with torch.no_grad():
            return self.encoder(x)