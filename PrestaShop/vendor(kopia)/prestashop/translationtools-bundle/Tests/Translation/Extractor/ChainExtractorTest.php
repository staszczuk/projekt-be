<?php

namespace PrestaShop\TranslationToolsBundle\Tests\Translation\Extractor;

use PrestaShop\TranslationToolsBundle\Tests\PhpUnit\TestCase;
use PrestaShop\TranslationToolsBundle\Translation\Extractor\ChainExtractor;
use Symfony\Component\Translation\MessageCatalogue;

class ChainExtractorTest extends TestCase
{
    protected $instance;

    public function setUp(): void
    {
        $this->instance = new ChainExtractor();
    }

    public function tearDown(): void
    {
        $this->instance = null;
    }

    public function testAddExtractor()
    {
        $extractor = $this->getMockBuilder('Symfony\Component\Translation\Extractor\ExtractorInterface')
            ->getMock()
        ;
        $this->assertSame($this->instance, $this->instance->addExtractor('test', $extractor));
    }

    public function testExtract()
    {
        $directory = '/';
        $catalog = new MessageCatalogue('en', []);
        $extractor = $this->getMockBuilder('Symfony\Component\Translation\Extractor\ExtractorInterface')
            ->setMethods(['setFinder', 'extract', 'setPrefix'])
            ->disableOriginalConstructor()
            ->disableOriginalClone()
            ->disableArgumentCloning()
            ->getMock();

        $extractor->expects($this->once())->method('setFinder');
        $extractor->expects($this->once())
            ->method('extract')
            ->with($directory, $catalog);

        $this->instance->addExtractor('test', $extractor);
        $this->instance->extract($directory, $catalog);
    }
}
