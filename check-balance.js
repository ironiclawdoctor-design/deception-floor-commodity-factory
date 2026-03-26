const { createPublicClient, http } = require('viem');
const { base } = require('viem/chains');

// Create client for Base network
const client = createPublicClient({
  chain: base,
  transport: http('https://mainnet.base.org'),
});

async function checkBalance() {
  try {
    const address = '0x499516cBE49262be42452438E7E202bF8fa79615';
    
    console.log('Checking wallet balance on Base network...');
    console.log('Address:', address);
    
    const balance = await client.getBalance({
      address: address,
    });
    
    console.log('Balance in wei:', balance.toString());
    
    // Convert to ETH (1 ETH = 10^18 wei)
    const ethBalance = Number(balance) / 10**18;
    console.log('Balance in ETH:', ethBalance.toFixed(18));
    
    if (ethBalance > 0) {
      console.log('✅ ETH balance detected!');
      console.log('Proceeding with MoltStation registration would be possible.');
    } else {
      console.log('❌ No ETH balance detected.');
      console.log('MoltStation registration requires ETH for gas fees.');
    }
    
  } catch (error) {
    console.error('Error checking balance:', error.message);
  }
}

checkBalance();