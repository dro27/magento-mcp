<?php

namespace Mcp\LlamaMcp\Block\Adminhtml;


use Magento\Backend\Block\Template;


class Chat extends Template
{
    protected function _prepareLayout()
    {
        $this->setTemplate('Mcp_LlamaMcp::chat.phtml');
        return parent::_prepareLayout();
    }
}
