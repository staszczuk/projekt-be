<?php

namespace PrestaShop\TranslationToolsBundle\Tests\Translation;

use PrestaShop\TranslationToolsBundle\Tests\PhpUnit\TestCase;
use PrestaShop\TranslationToolsBundle\Translation\MultilanguageCatalog;

class MultilanguageCatalogTest extends TestCase
{
    protected $instance;

    public function setUp(): void
    {
        $this->instance = new MultilanguageCatalog();
    }

    public function tearDown(): void
    {
        $this->instance = null;
    }

    public function testGetSetHas()
    {
        $this->assertEquals(false, $this->instance->has('key'));
        $this->assertSame($this->instance, $this->instance->set('key', 'locale', 'translation'));
        $this->assertEquals(true, $this->instance->has('key'));
        $this->assertEquals(['locale' => 'translation'], $this->instance->get('key'));
        $this->assertEquals(true, $this->instance->has('key', 'locale'));
        $this->assertEquals('translation', $this->instance->get('key', 'locale'));
    }
}
