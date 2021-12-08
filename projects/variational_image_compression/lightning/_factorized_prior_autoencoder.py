# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import torch.hub

import neuralcompression.models
from ._prior_autoencoder import _PriorAutoencoder


class FactorizedPriorAutoencoder(_PriorAutoencoder):
    """Factorized prior autoencoder described in:

        | End-to-end Optimized Image Compression
        | Johannes Ballé, Valero Laparra, Eero P. Simoncelli
        | https://arxiv.org/abs/1611.01704

    Args:
        network_channels: number of channels in the network.
        compression_channels: number of inferred latent compression features.
        in_channels: number of channels in the input image.
        distortion_trade_off: rate-distortion trade-off. :math:`trade = 1` is
            the solution where :math:`(rate, distortion)` minimizes
            :math:`rate + distortion`. Increasing `trade_off` will penalize the
            distortion term so more bits are spent.
        optimizer_lr: learning rate for the autoencoder optimizer.
        bottleneck_optimizer_lr: learning rate for the bottleneck optimizer.
        pretrained: load weights from model pre-trained on
            ``neuralcompression.datavimeo90k``.
    """

    network: neuralcompression.models.FactorizedPriorAutoencoder

    def __init__(
        self,
        network_channels: int = 128,
        compression_channels: int = 192,
        in_channels: int = 3,
        distortion_trade_off: float = 1e-2,
        optimizer_lr: float = 1e-3,
        bottleneck_optimizer_lr: float = 1e-3,
        pretrained: bool = False,
    ):
        super(FactorizedPriorAutoencoder, self).__init__(
            distortion_trade_off,
            optimizer_lr,
            bottleneck_optimizer_lr,
        )

        self.network = neuralcompression.models.FactorizedPriorAutoencoder(
            network_channels,
            compression_channels,
            in_channels,
        )

        if pretrained:
            url = (
                "https://dl.fbaipublicfiles.com"
                + "/"
                + "neuralcompression"
                + "/"
                + "models"
                + "/"
                + "factorized_prior"
                + "_"
                + "vimeo_90k"
                + "_"
                + "mse"
                + "_"
                + str(network_channels)
                + "_"
                + str(compression_channels)
                + "_"
                + str(distortion_trade_off).replace(".", "_")
                + ".pth"
            )

            state_dict = torch.hub.load_state_dict_from_url(url)

            self.network.load_state_dict(state_dict)
