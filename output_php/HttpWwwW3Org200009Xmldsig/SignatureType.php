<?php

namespace Generated\HttpWwwW3Org200009Xmldsig;

/**
 * Class representing SignatureType
 *
 * 
 * XSD Type: SignatureType
 */
class SignatureType
{
    /**
     * @var string $id
     */
    private $id = null;

    /**
     * @var \Generated\HttpWwwW3Org200009Xmldsig\SignedInfo $signedInfo
     */
    private $signedInfo = null;

    /**
     * @var \Generated\HttpWwwW3Org200009Xmldsig\SignatureValue $signatureValue
     */
    private $signatureValue = null;

    /**
     * @var \Generated\HttpWwwW3Org200009Xmldsig\KeyInfo $keyInfo
     */
    private $keyInfo = null;

    /**
     * @var \Generated\HttpWwwW3Org200009Xmldsig\ObjectXsd[] $object
     */
    private $object = [
        
    ];

    /**
     * Gets as id
     *
     * @return string
     */
    public function getId()
    {
        return $this->id;
    }

    /**
     * Sets a new id
     *
     * @param string $id
     * @return self
     */
    public function setId($id)
    {
        $this->id = $id;
        return $this;
    }

    /**
     * Gets as signedInfo
     *
     * @return \Generated\HttpWwwW3Org200009Xmldsig\SignedInfo
     */
    public function getSignedInfo()
    {
        return $this->signedInfo;
    }

    /**
     * Sets a new signedInfo
     *
     * @param \Generated\HttpWwwW3Org200009Xmldsig\SignedInfo $signedInfo
     * @return self
     */
    public function setSignedInfo(\Generated\HttpWwwW3Org200009Xmldsig\SignedInfo $signedInfo)
    {
        $this->signedInfo = $signedInfo;
        return $this;
    }

    /**
     * Gets as signatureValue
     *
     * @return \Generated\HttpWwwW3Org200009Xmldsig\SignatureValue
     */
    public function getSignatureValue()
    {
        return $this->signatureValue;
    }

    /**
     * Sets a new signatureValue
     *
     * @param \Generated\HttpWwwW3Org200009Xmldsig\SignatureValue $signatureValue
     * @return self
     */
    public function setSignatureValue(\Generated\HttpWwwW3Org200009Xmldsig\SignatureValue $signatureValue)
    {
        $this->signatureValue = $signatureValue;
        return $this;
    }

    /**
     * Gets as keyInfo
     *
     * @return \Generated\HttpWwwW3Org200009Xmldsig\KeyInfo
     */
    public function getKeyInfo()
    {
        return $this->keyInfo;
    }

    /**
     * Sets a new keyInfo
     *
     * @param \Generated\HttpWwwW3Org200009Xmldsig\KeyInfo $keyInfo
     * @return self
     */
    public function setKeyInfo(?\Generated\HttpWwwW3Org200009Xmldsig\KeyInfo $keyInfo = null)
    {
        $this->keyInfo = $keyInfo;
        return $this;
    }

    /**
     * Adds as object
     *
     * @return self
     * @param \Generated\HttpWwwW3Org200009Xmldsig\ObjectXsd $object
     */
    public function addToObject(\Generated\HttpWwwW3Org200009Xmldsig\ObjectXsd $object)
    {
        $this->object[] = $object;
        return $this;
    }

    /**
     * isset object
     *
     * @param int|string $index
     * @return bool
     */
    public function issetObject($index)
    {
        return isset($this->object[$index]);
    }

    /**
     * unset object
     *
     * @param int|string $index
     * @return void
     */
    public function unsetObject($index)
    {
        unset($this->object[$index]);
    }

    /**
     * Gets as object
     *
     * @return \Generated\HttpWwwW3Org200009Xmldsig\ObjectXsd[]
     */
    public function getObject()
    {
        return $this->object;
    }

    /**
     * Sets a new object
     *
     * @param \Generated\HttpWwwW3Org200009Xmldsig\ObjectXsd[] $object
     * @return self
     */
    public function setObject(?array $object = null)
    {
        $this->object = $object;
        return $this;
    }
}

