import { useState, useEffect } from "react";
import {
  Box,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
  Spinner,
  Input,
  Flex,
  IconButton,
  InputGroup,
  InputLeftElement,
  Select,
} from "@chakra-ui/react";
import axios from "axios";
import { createFileRoute } from "@tanstack/react-router";
import { FiSearch, FiRefreshCw } from "react-icons/fi";

interface DNSRecord {
  id: string;
  type: string;
  name: string;
  value: string;
  timestamp: string;
}

export const Route = createFileRoute("/_layout/dns-records")({
  component: DNSRecords,
});

function DNSRecords() {
  const [records, setRecords] = useState<DNSRecord[]>([]);
  const [filteredRecords, setFilteredRecords] = useState<DNSRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [filterType, setFilterType] = useState("all");

  useEffect(() => {
    const fetchRecords = async () => {
      try {
        const response = await axios.get("/api/v1/dns");
        setRecords(response.data);
        setFilteredRecords(response.data);
      } catch (error) {
        console.error("Error fetching DNS records:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecords();
  }, []);

  // Filter and search functionality
  useEffect(() => {
    let updatedRecords = records;

    if (filterType !== "all") {
      updatedRecords = updatedRecords.filter(
        (record) => record.type.toLowerCase() === filterType.toLowerCase()
      );
    }

    if (search) {
      updatedRecords = updatedRecords.filter((record) =>
        record.name.toLowerCase().includes(search.toLowerCase())
      );
    }

    setFilteredRecords(updatedRecords);
  }, [search, filterType, records]);

  if (loading) {
    return (
      <Box textAlign="center" p={6}>
        <Spinner size="xl" />
        <Heading size="md" mt={4}>
          Loading DNS Records...
        </Heading>
      </Box>
    );
  }

  return (
    <Box p={6}>
      <Flex justifyContent="space-between" alignItems="center" mb={4}>
        <Heading>DNS Records</Heading>
        <IconButton
          aria-label="Refresh"
          icon={<FiRefreshCw />}
          onClick={() => window.location.reload()}
        />
      </Flex>

      <Flex mb={4} gap={4}>
        {/* Search Bar with FiSearch Icon */}
        <InputGroup maxW="300px">
          <InputLeftElement pointerEvents="none">
            <FiSearch color="gray" />
          </InputLeftElement>
          <Input
            placeholder="Search by name..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </InputGroup>

        {/* Filter Dropdown */}
        <Select
          placeholder="Filter by type"
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          maxW="200px"
        >
          <option value="all">All</option>
          <option value="A">A</option>
          <option value="CNAME">CNAME</option>
          <option value="MX">MX</option>
        </Select>
      </Flex>

      {/* Table Layout */}
      <Table variant="striped" colorScheme="teal" size="md">
        <Thead>
          <Tr>
            <Th>ID</Th>
            <Th>Type</Th>
            <Th>Name</Th>
            <Th>Value</Th>
            <Th>Timestamp</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {filteredRecords.map((record) => (
            <Tr key={record.id}>
              <Td>{record.id}</Td>
              <Td>{record.type}</Td>
              <Td>{record.name}</Td>
              <Td>{record.value}</Td>
              <Td>{new Date(record.timestamp).toLocaleString()}</Td>
              <Td>
                <Button colorScheme="blue" size="sm" mr={2}>
                  Edit
                </Button>
                <Button colorScheme="red" size="sm">
                  Delete
                </Button>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
}

export default DNSRecords;
