<?php

namespace Mcp\LlamaMcp\Helper;

use Magento\Framework\App\Helper\AbstractHelper;
use Magento\Framework\HTTP\Client\Curl;
use Psr\Log\LoggerInterface;

class McpClientHelper extends AbstractHelper
{
    protected $curl;
    protected $logger;

    public function __construct(Curl $curl, LoggerInterface $logger)
    {
        $this->curl = $curl;
        $this->logger = $logger;
    }

    public function sendToClaude($prompt)
    {
        $cmd = escapeshellcmd("/var/www/html/venv-mcp/bin/python /var/www/html/app/code/Mcp/LlamaMcp/mcp_claude_bridge.py \"$prompt\"");
        exec($cmd, $output, $returnCode);

        if ($returnCode !== 0) {
            return ['error' => 'MCP helper failed', 'output' => implode("\n", $output)];
        }

        $this->logger()->info(print_r($output, true));

        return json_decode(implode("\n", $output), true);
    }

    private function logger()
    {
        $writer = new \Zend_Log_Writer_Stream(BP . '/var/log/mcp-error-' . date('Y-m-d') . '.log');
        $logger = new \Zend_Log();
        return $logger->addWriter($writer);
    }
}
