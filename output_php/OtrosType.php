<?php

namespace Generated;

/**
 * Class representing OtrosType
 *
 * 
 * XSD Type: OtrosType
 */
class OtrosType
{
    /**
     * Elemento opcional que se puede utilizar para almacenar texto.
     *
     * @var \Generated\OtroTextoType[] $otroTexto
     */
    private $otroTexto = [
        
    ];

    /**
     * Elemento opcional que se puede utilizar para almacenar texto.
     *
     * @var \Generated\OtroTextoType[] $otroContenido
     */
    private $otroContenido = [
        
    ];

    /**
     * Adds as otroTexto
     *
     * Elemento opcional que se puede utilizar para almacenar texto.
     *
     * @return self
     * @param \Generated\OtroTextoType $otroTexto
     */
    public function addToOtroTexto(\Generated\OtroTextoType $otroTexto)
    {
        $this->otroTexto[] = $otroTexto;
        return $this;
    }

    /**
     * isset otroTexto
     *
     * Elemento opcional que se puede utilizar para almacenar texto.
     *
     * @param int|string $index
     * @return bool
     */
    public function issetOtroTexto($index)
    {
        return isset($this->otroTexto[$index]);
    }

    /**
     * unset otroTexto
     *
     * Elemento opcional que se puede utilizar para almacenar texto.
     *
     * @param int|string $index
     * @return void
     */
    public function unsetOtroTexto($index)
    {
        unset($this->otroTexto[$index]);
    }

    /**
     * Gets as otroTexto
     *
     * Elemento opcional que se puede utilizar para almacenar texto.
     *
     * @return \Generated\OtroTextoType[]
     */
    public function getOtroTexto()
    {
        return $this->otroTexto;
    }

    /**
     * Sets a new otroTexto
     *
     * Elemento opcional que se puede utilizar para almacenar texto.
     *
     * @param \Generated\OtroTextoType[] $otroTexto
     * @return self
     */
    public function setOtroTexto(?array $otroTexto = null)
    {
        $this->otroTexto = $otroTexto;
        return $this;
    }

    /**
     * Adds as otroContenido
     *
     * Elemento opcional que se puede utilizar para almacenar texto.
     *
     * @return self
     * @param \Generated\OtroTextoType $otroContenido
     */
    public function addToOtroContenido(\Generated\OtroTextoType $otroContenido)
    {
        $this->otroContenido[] = $otroContenido;
        return $this;
    }

    /**
     * isset otroContenido
     *
     * Elemento opcional que se puede utilizar para almacenar texto.
     *
     * @param int|string $index
     * @return bool
     */
    public function issetOtroContenido($index)
    {
        return isset($this->otroContenido[$index]);
    }

    /**
     * unset otroContenido
     *
     * Elemento opcional que se puede utilizar para almacenar texto.
     *
     * @param int|string $index
     * @return void
     */
    public function unsetOtroContenido($index)
    {
        unset($this->otroContenido[$index]);
    }

    /**
     * Gets as otroContenido
     *
     * Elemento opcional que se puede utilizar para almacenar texto.
     *
     * @return \Generated\OtroTextoType[]
     */
    public function getOtroContenido()
    {
        return $this->otroContenido;
    }

    /**
     * Sets a new otroContenido
     *
     * Elemento opcional que se puede utilizar para almacenar texto.
     *
     * @param \Generated\OtroTextoType[] $otroContenido
     * @return self
     */
    public function setOtroContenido(?array $otroContenido = null)
    {
        $this->otroContenido = $otroContenido;
        return $this;
    }
}

