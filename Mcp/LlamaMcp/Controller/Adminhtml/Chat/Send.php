<?php

namespace Mcp\LlamaMcp\Controller\Adminhtml\Chat;


use Magento\Backend\App\Action;
use Mcp\LlamaMcp\Helper\McpClientHelper;
use Magento\Framework\Controller\Result\JsonFactory;

class Send extends Action
{
    protected $mcpHelper;
    protected $jsonFactory;

    public function __construct(
        Action\Context $context,
        McpClientHelper $mcpHelper,
        JsonFactory $jsonFactory
    ) {
        parent::__construct($context);
        $this->mcpHelper = $mcpHelper;
        $this->jsonFactory = $jsonFactory;
    }

    public function execute()
    {
        $resultJson = $this->jsonFactory->create();
        $prompt = $this->getRequest()->getParam('prompt');

        if (!$prompt) {
            return $resultJson->setData(['error' => 'Missing prompt parameter']);
        }

        $response = $this->mcpHelper->sendToClaude($prompt);

        return $resultJson->setData(['response' => $response ?: 'MCP helper failed']);
    }
}
