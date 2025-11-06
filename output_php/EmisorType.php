<?php

namespace Generated;

/**
 * Class representing EmisorType
 *
 * 
 * XSD Type: EmisorType
 */
class EmisorType
{
    /**
     * Nombre o razon social
     *
     * @var string $nombre
     */
    private $nombre = null;

    /**
     * @var \Generated\IdentificacionType $identificacion
     */
    private $identificacion = null;

    /**
     * Campo condicional. Se convierte en carácter obligatorio cuando se
     * estén facturando códigosCAByS de bebidas alcohólicas según la Ley
     * 8707. Contiene los datos del número de registro de bebidas
     * alcohólicas, suministrado por la Dirección General de Aduanas
     *
     * @var string $registrofiscal8707
     */
    private $registrofiscal8707 = null;

    /**
     * En caso de que se cuente con nombre comercial debe indicarse
     *
     * @var string $nombreComercial
     */
    private $nombreComercial = null;

    /**
     * @var \Generated\UbicacionType $ubicacion
     */
    private $ubicacion = null;

    /**
     * @var \Generated\TelefonoType $telefono
     */
    private $telefono = null;

    /**
     * Debe cumplir con la siguiente estructura: 
     *  \s*\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*\s*
     *
     * @var string[] $correoElectronico
     */
    private $correoElectronico = [
        
    ];

    /**
     * Gets as nombre
     *
     * Nombre o razon social
     *
     * @return string
     */
    public function getNombre()
    {
        return $this->nombre;
    }

    /**
     * Sets a new nombre
     *
     * Nombre o razon social
     *
     * @param string $nombre
     * @return self
     */
    public function setNombre($nombre)
    {
        $this->nombre = $nombre;
        return $this;
    }

    /**
     * Gets as identificacion
     *
     * @return \Generated\IdentificacionType
     */
    public function getIdentificacion()
    {
        return $this->identificacion;
    }

    /**
     * Sets a new identificacion
     *
     * @param \Generated\IdentificacionType $identificacion
     * @return self
     */
    public function setIdentificacion(\Generated\IdentificacionType $identificacion)
    {
        $this->identificacion = $identificacion;
        return $this;
    }

    /**
     * Gets as registrofiscal8707
     *
     * Campo condicional. Se convierte en carácter obligatorio cuando se
     * estén facturando códigosCAByS de bebidas alcohólicas según la Ley
     * 8707. Contiene los datos del número de registro de bebidas
     * alcohólicas, suministrado por la Dirección General de Aduanas
     *
     * @return string
     */
    public function getRegistrofiscal8707()
    {
        return $this->registrofiscal8707;
    }

    /**
     * Sets a new registrofiscal8707
     *
     * Campo condicional. Se convierte en carácter obligatorio cuando se
     * estén facturando códigosCAByS de bebidas alcohólicas según la Ley
     * 8707. Contiene los datos del número de registro de bebidas
     * alcohólicas, suministrado por la Dirección General de Aduanas
     *
     * @param string $registrofiscal8707
     * @return self
     */
    public function setRegistrofiscal8707($registrofiscal8707)
    {
        $this->registrofiscal8707 = $registrofiscal8707;
        return $this;
    }

    /**
     * Gets as nombreComercial
     *
     * En caso de que se cuente con nombre comercial debe indicarse
     *
     * @return string
     */
    public function getNombreComercial()
    {
        return $this->nombreComercial;
    }

    /**
     * Sets a new nombreComercial
     *
     * En caso de que se cuente con nombre comercial debe indicarse
     *
     * @param string $nombreComercial
     * @return self
     */
    public function setNombreComercial($nombreComercial)
    {
        $this->nombreComercial = $nombreComercial;
        return $this;
    }

    /**
     * Gets as ubicacion
     *
     * @return \Generated\UbicacionType
     */
    public function getUbicacion()
    {
        return $this->ubicacion;
    }

    /**
     * Sets a new ubicacion
     *
     * @param \Generated\UbicacionType $ubicacion
     * @return self
     */
    public function setUbicacion(\Generated\UbicacionType $ubicacion)
    {
        $this->ubicacion = $ubicacion;
        return $this;
    }

    /**
     * Gets as telefono
     *
     * @return \Generated\TelefonoType
     */
    public function getTelefono()
    {
        return $this->telefono;
    }

    /**
     * Sets a new telefono
     *
     * @param \Generated\TelefonoType $telefono
     * @return self
     */
    public function setTelefono(?\Generated\TelefonoType $telefono = null)
    {
        $this->telefono = $telefono;
        return $this;
    }

    /**
     * Adds as correoElectronico
     *
     * Debe cumplir con la siguiente estructura: 
     *  \s*\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*\s*
     *
     * @return self
     * @param string $correoElectronico
     */
    public function addToCorreoElectronico($correoElectronico)
    {
        $this->correoElectronico[] = $correoElectronico;
        return $this;
    }

    /**
     * isset correoElectronico
     *
     * Debe cumplir con la siguiente estructura: 
     *  \s*\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*\s*
     *
     * @param int|string $index
     * @return bool
     */
    public function issetCorreoElectronico($index)
    {
        return isset($this->correoElectronico[$index]);
    }

    /**
     * unset correoElectronico
     *
     * Debe cumplir con la siguiente estructura: 
     *  \s*\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*\s*
     *
     * @param int|string $index
     * @return void
     */
    public function unsetCorreoElectronico($index)
    {
        unset($this->correoElectronico[$index]);
    }

    /**
     * Gets as correoElectronico
     *
     * Debe cumplir con la siguiente estructura: 
     *  \s*\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*\s*
     *
     * @return string[]
     */
    public function getCorreoElectronico()
    {
        return $this->correoElectronico;
    }

    /**
     * Sets a new correoElectronico
     *
     * Debe cumplir con la siguiente estructura: 
     *  \s*\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*\s*
     *
     * @param string $correoElectronico
     * @return self
     */
    public function setCorreoElectronico(array $correoElectronico)
    {
        $this->correoElectronico = $correoElectronico;
        return $this;
    }
}

