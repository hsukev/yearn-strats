// SPDX-License-Identifier: AGPL-3.0
pragma solidity >=0.6.0 <0.7.0;
pragma experimental ABIEncoderV2;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";

interface ICurveStrategyProxy {
    function approveStrategy(address _gauge, address _strategy) external;

    function revokeStrategy(address _gauge) external;

    function withdraw(
        address _gauge,
        address _token,
        uint256 _amount
    ) external returns (uint256);

    function balanceOf(address _gauge) external view returns (uint256);

    function withdrawAll(address _gauge, address _token) external returns (uint256);

    function deposit(address _gauge, address _token) external;

    function harvest(address _gauge) external;

    function claim(address recipient) external;
}

interface IKeep3rV1Oracle {
    function current(
        address tokenIn,
        uint256 amountIn,
        address tokenOut
    ) external view returns (uint256 amountOut);
}
